import tensorflow as tf
import numpy as np
from tensorflow.keras import layers

class VQVAE(tf.keras.Model):
    def __init__(self, latent_dim, num_embeddings, embedding_dim):
        super(VQVAE, self).__init__()
        self.latent_dim = latent_dim
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim

        # Encoder
        self.encoder = tf.keras.Sequential([
            layers.Input(shape=(28, 28, 1)),
            layers.Conv2D(32, 3, activation='relu', strides=2, padding='same'),
            layers.Conv2D(64, 3, activation='relu', strides=2, padding='same'),
            layers.Flatten(),
            layers.Dense(embedding_dim)
        ])

        # Vector Quantizer
        self.vq_layer = VectorQuantizer(num_embeddings, embedding_dim)

        # Decoder
        self.decoder = tf.keras.Sequential([
            layers.Input(shape=(embedding_dim,)),
            layers.Dense(7 * 7 * 32, activation='relu'),
            layers.Reshape((7, 7, 32)),
            layers.Conv2DTranspose(64, 3, activation='relu', strides=2, padding='same'),
            layers.Conv2DTranspose(32, 3, activation='relu', strides=2, padding='same'),
            layers.Conv2DTranspose(1, 3, activation='sigmoid', padding='same')
        ])

    def call(self, inputs):
        encoded = self.encoder(inputs)
        quantized, vq_loss = self.vq_layer(encoded)
        reconstructed = self.decoder(quantized)
        return reconstructed, vq_loss

class VectorQuantizer(layers.Layer):
    def __init__(self, num_embeddings, embedding_dim):
        super(VectorQuantizer, self).__init__()
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim
        self.embeddings = self.add_weight(
            shape=(num_embeddings, embedding_dim),
            initializer='random_normal',
            trainable=True,
            name='embeddings'
        )

    def call(self, inputs):
        # Flatten input except for last dimension
        flat_inputs = tf.reshape(inputs, (-1, self.embedding_dim))

        # Calculate distances
        distances = (tf.reduce_sum(flat_inputs**2, axis=1, keepdims=True) 
                     + tf.reduce_sum(self.embeddings**2, axis=1)
                     - 2 * tf.matmul(flat_inputs, self.embeddings, transpose_b=True))

        # Encoding
        encoding_indices = tf.argmin(distances, axis=1)
        encodings = tf.one_hot(encoding_indices, self.num_embeddings)

        # Quantize
        quantized = tf.matmul(encodings, self.embeddings)

        # Reshape to match input shape
        quantized = tf.reshape(quantized, tf.shape(inputs))

        # Compute loss
        e_latent_loss = tf.reduce_mean((tf.stop_gradient(quantized) - inputs) ** 2)
        q_latent_loss = tf.reduce_mean((quantized - tf.stop_gradient(inputs)) ** 2)
        vq_loss = q_latent_loss + tf.stop_gradient(e_latent_loss)

        quantized = inputs + tf.stop_gradient(quantized - inputs)
        return quantized, vq_loss

def compute_loss(model, x):
    reconstructed, vq_loss = model(x)
    reconstruction_loss = tf.reduce_mean(
        tf.reduce_sum(tf.keras.losses.binary_crossentropy(x, reconstructed), axis=(1, 2))
    )
    total_loss = reconstruction_loss + vq_loss
    return total_loss, reconstruction_loss, vq_loss

@tf.function
def train_step(model, x, optimizer):
    with tf.GradientTape() as tape:
        total_loss, reconstruction_loss, vq_loss = compute_loss(model, x)
    gradients = tape.gradient(total_loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return total_loss, reconstruction_loss, vq_loss

# Load and preprocess data
(x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1))
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1))

# Model parameters
latent_dim = 16
num_embeddings = 64
embedding_dim = 64

# Create and train model
vqvae = VQVAE(latent_dim, num_embeddings, embedding_dim)
optimizer = tf.keras.optimizers.Adam(1e-3)

epochs = 10
batch_size = 32
train_dataset = tf.data.Dataset.from_tensor_slices(x_train).shuffle(x_train.shape[0]).batch(batch_size)

for epoch in range(epochs):
    total_loss_avg = tf.keras.metrics.Mean()
    reconstruction_loss_avg = tf.keras.metrics.Mean()
    vq_loss_avg = tf.keras.metrics.Mean()

    for batch in train_dataset:
        total_loss, reconstruction_loss, vq_loss = train_step(vqvae, batch, optimizer)
        total_loss_avg.update_state(total_loss)
        reconstruction_loss_avg.update_state(reconstruction_loss)
        vq_loss_avg.update_state(vq_loss)

    print(f'Epoch {epoch + 1}, '
          f'Loss: {total_loss_avg.result():.4f}, '
          f'Reconstruction Loss: {reconstruction_loss_avg.result():.4f}, '
          f'VQ Loss: {vq_loss_avg.result():.4f}')

# Generate new samples
num_samples = 16
random_vectors = tf.random.uniform(shape=[num_samples, embedding_dim], minval=0, maxval=1)
quantized_vectors, _ = vqvae.vq_layer(random_vectors)
generated_images = vqvae.decoder(quantized_vectors)

print("Generated images shape:", generated_images.shape)
print("Sample generated image min and max values:")
print(tf.reduce_min(generated_images), tf.reduce_max(generated_images))
