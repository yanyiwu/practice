import tensorflow as tf
import numpy as np
from tensorflow.keras import layers

class VAE(tf.keras.Model):
    def __init__(self, latent_dim):
        super(VAE, self).__init__()
        self.latent_dim = latent_dim
        self.encoder = tf.keras.Sequential([
            layers.Input(shape=(28, 28, 1)),
            layers.Conv2D(32, 3, activation='relu', strides=2, padding='same'),
            layers.Conv2D(64, 3, activation='relu', strides=2, padding='same'),
            layers.Flatten(),
            layers.Dense(16, activation='relu'),
            layers.Dense(latent_dim * 2)
        ])

        self.decoder = tf.keras.Sequential([
            layers.Input(shape=(latent_dim,)),
            layers.Dense(7 * 7 * 32, activation='relu'),
            layers.Reshape((7, 7, 32)),
            layers.Conv2DTranspose(64, 3, activation='relu', strides=2, padding='same'),
            layers.Conv2DTranspose(32, 3, activation='relu', strides=2, padding='same'),
            layers.Conv2DTranspose(1, 3, activation='sigmoid', padding='same')
        ])

    def encode(self, x):
        mean, logvar = tf.split(self.encoder(x), num_or_size_splits=2, axis=1)
        return mean, logvar

    def reparameterize(self, mean, logvar):
        eps = tf.random.normal(shape=mean.shape)
        return eps * tf.exp(logvar * .5) + mean

    def decode(self, z):
        return self.decoder(z)

    def call(self, inputs):
        mean, logvar = self.encode(inputs)
        z = self.reparameterize(mean, logvar)
        reconstructed = self.decode(z)
        return reconstructed, mean, logvar

def compute_loss(model, x):
    reconstructed, mean, logvar = model(x)
    reconstruction_loss = tf.reduce_mean(
        tf.reduce_sum(tf.keras.losses.binary_crossentropy(x, reconstructed), axis=(1, 2))
    )
    kl_loss = -0.5 * tf.reduce_mean(1 + logvar - tf.square(mean) - tf.exp(logvar))
    total_loss = reconstruction_loss + kl_loss
    return total_loss

@tf.function
def train_step(model, x, optimizer):
    with tf.GradientTape() as tape:
        loss = compute_loss(model, x)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss

# Load and preprocess the MNIST dataset
(x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1))
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1))

# Create and train the VAE model
latent_dim = 2
vae = VAE(latent_dim)
optimizer = tf.keras.optimizers.Adam(1e-4)

epochs = 10
batch_size = 32
train_dataset = tf.data.Dataset.from_tensor_slices(x_train).shuffle(x_train.shape[0]).batch(batch_size)

for epoch in range(epochs):
    for batch in train_dataset:
        loss = train_step(vae, batch, optimizer)
    print(f'Epoch {epoch + 1}, Loss: {loss.numpy():.4f}')

# Generate some samples
num_samples = 16
random_vector = tf.random.normal(shape=[num_samples, latent_dim])
generated_images = vae.decode(random_vector)

print("Generated images shape:", generated_images.shape)
print("Sample generated image min and max values:")
print(tf.reduce_min(generated_images), tf.reduce_max(generated_images))
