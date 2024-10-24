import tensorflow as tf
import numpy as np
from tensorflow.keras import layers

# VQVAE (Vector Quantized Variational Autoencoder)
# 核心思想：将连续的潜在空间离散化，通过向量量化来实现
# 与VAE的主要区别：
# 1. VQVAE使用离散的潜在表示，而VAE使用连续的潜在表示
# 2. VQVAE不需要重参数化技巧，而是使用向量量化
# 3. VQVAE的潜在空间更加结构化，有利于生成高质量样本
class VQVAE(tf.keras.Model):
    def __init__(self, latent_dim, num_embeddings, embedding_dim):
        super(VQVAE, self).__init__()
        self.latent_dim = latent_dim
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim

        # Encoder: 将输入压缩到潜在空间
        self.encoder = tf.keras.Sequential([
            layers.Input(shape=(28, 28, 1)),

            # (batch_size, 28, 28, 1) -> (batch_size, 14, 14, 32)
            layers.Conv2D(32, 3, activation='relu', strides=2, padding='same'),

            # (batch_size, 14, 14, 32) -> (batch_size, 7, 7, 64)
            layers.Conv2D(64, 3, activation='relu', strides=2, padding='same'),

            # (batch_size, 7, 7, 64) -> (batch_size, 7*7*64)
            layers.Flatten(),

            # (batch_size, 7*7*64) -> (batch_size, embedding_dim)
            layers.Dense(embedding_dim)
        ])

        # Vector Quantizer: 将连续的编码向量映射到离散的码本向量
        self.vq_layer = VectorQuantizer(num_embeddings, embedding_dim)

        # Decoder: 从量化的潜在表示重构输入
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
        # num_embeddings: 码本中向量的数量  
        self.embedding_dim = embedding_dim
        # embedding_dim: 码本中每个向量的维度

        # 初始化码本（codebook）
        self.embeddings = self.add_weight(
            shape=(num_embeddings, embedding_dim),
            initializer='random_normal',
            trainable=True,
            name='embeddings'
        )

    def call(self, inputs):
        # 直接使用 inputs
        # inputs shape: (batch_size, embedding_dim)
        # self.embeddings shape: (num_embeddings, embedding_dim)    
        distances = (tf.reduce_sum(inputs**2, axis=1, keepdims=True) 
                     + tf.reduce_sum(self.embeddings**2, axis=1)
                     - 2 * tf.matmul(inputs, self.embeddings, transpose_b=True))
        # distances shape: (batch_size, num_embeddings) 

        # 找到最近的码本向量
        encoding_indices = tf.argmin(distances, axis=1)
        # encoding_indices shape: (batch_size, )
        encodings = tf.one_hot(encoding_indices, self.num_embeddings)
        # encodings shape: (batch_size, num_embeddings) 
        # 量化：用最近的码本向量替换输入向量
        quantized = tf.matmul(encodings, self.embeddings)
        # quantized shape: (batch_size, embedding_dim)

        # 计算损失
        # e_latent_loss：确保编码器输出接近码本向量
        e_latent_loss = tf.reduce_mean((tf.stop_gradient(quantized) - inputs) ** 2)
        # q_latent_loss：确保码本向量接近编码器输出
        q_latent_loss = tf.reduce_mean((quantized - tf.stop_gradient(inputs)) ** 2)
        # vq_loss：总的向量量化损失
        vq_loss = q_latent_loss + tf.stop_gradient(e_latent_loss)

        # 使用直通估计器（straight-through estimator）来传递梯度
        # forward: quantized = quantized
        # backward: quantized = inputs  
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
# x_train shape: (60000, 28, 28)        
x_test = x_test.astype('float32') / 255.
# x_test shape: (10000, 28, 28) 
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1))
# x_train shape: (60000, 28, 28, 1)
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1))
# x_test shape: (10000, 28, 28, 1)

# Model parameters
latent_dim = 16
num_embeddings = 64
embedding_dim = 128

# Create and train model
vqvae = VQVAE(latent_dim, num_embeddings, embedding_dim)
optimizer = tf.keras.optimizers.Adam(1e-3)

epochs = 2
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
