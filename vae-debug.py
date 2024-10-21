import tensorflow as tf
import numpy as np
from tensorflow.keras import layers

class VAE(tf.keras.Model):
    def __init__(self, latent_dim):
        super(VAE, self).__init__()
        self.latent_dim = latent_dim
        # 核心思想: 编码器将输入压缩到低维潜在空间
        self.encoder = tf.keras.Sequential([
            layers.Input(shape=(28, 28, 1)),

            layers.Conv2D(32, 3, activation='relu', strides=2, padding='same'),
            # (28, 28, 1) -> (14, 14, 32)   

            layers.Conv2D(64, 3, activation='relu', strides=2, padding='same'),
            # (14, 14, 32) -> (7, 7, 64)

            layers.Flatten(),
            # (7, 7, 64) -> (3136)

            layers.Dense(16, activation='relu'),
            # (3136) -> (16)

            layers.Dense(latent_dim * 2)
            # (16) -> (latent_dim * 2)  
        ])

        # 核心思想: 解码器从潜在空间重构输入
        self.decoder = tf.keras.Sequential([
            layers.Input(shape=(latent_dim,)),
            layers.Dense(7 * 7 * 32, activation='relu'),
            layers.Reshape((7, 7, 32)),
            layers.Conv2DTranspose(64, 3, activation='relu', strides=2, padding='same'),
            layers.Conv2DTranspose(32, 3, activation='relu', strides=2, padding='same'),
            layers.Conv2DTranspose(1, 3, activation='sigmoid', padding='same')
        ])

    # 核心思想: 将输入编码为均值和对数方差
    def encode(self, x):
        mean, logvar = tf.split(self.encoder(x), num_or_size_splits=2, axis=-1)
        return mean, logvar

    # 核心思想: 重参数化技巧,使得反向传播可行
    def reparameterize(self, mean, logvar):
        eps = tf.random.normal(shape=mean.shape)
        return eps * tf.exp(logvar * .5) + mean

    # 核心思想: 从潜在空间生成新样本
    def decode(self, z):
        return self.decoder(z)

    # 改进点: 可以考虑使用更复杂的编码器/解码器结构,如ResNet或Transformer
    def call(self, inputs):
        mean, logvar = self.encode(inputs)
        z = self.reparameterize(mean, logvar)
        reconstructed = self.decode(z)
        return reconstructed, mean, logvar

def compute_loss(model, x):
    # x shape: (32, 28, 28, 1)  
    reconstructed, mean, logvar = model(x)
    # reconstructed shape: (32, 28, 28, 1)
    # mean shape: (32, 16)
    # logvar shape: (32, 16)
    # 核心思想: 损失函数包括重构误差和KL散度
    # 改进点: 可以尝试其他重构损失,如感知损失或特征匹配
    reconstruction_loss = tf.reduce_mean(
        tf.reduce_sum(tf.keras.losses.binary_crossentropy(x, reconstructed), axis=(1, 2))
    )
    # 改进点: 可以使用更复杂的先验分布,如标准正态分布以外的分布
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

# 改进点: 可以考虑使用更大的数据集或更复杂的数据增强技术
(x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()
x_train = x_train.astype('float32') / 255.
# x_train shape: (60000, 28, 28)            
x_test = x_test.astype('float32') / 255.
# x_test shape: (10000, 28, 28)
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1))
# x_train shape: (60000, 28, 28, 1)
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1))
# x_test shape: (10000, 28, 28, 1)

# 改进点: 可以尝试不同的潜在空间维度,以平衡重构质量和生成多样性
latent_dim = 2
vae = VAE(latent_dim)
# 改进点: 可以尝试不同的优化器或学习率调度策略
optimizer = tf.keras.optimizers.Adam(1e-4)

# 改进点: 可以增加训练轮数,使用早停等技术防止过拟合
epochs = 4
batch_size = 32
train_dataset = tf.data.Dataset.from_tensor_slices(x_train).shuffle(x_train.shape[0]).batch(batch_size)

for epoch in range(epochs):
    for batch in train_dataset:
        loss = train_step(vae, batch, optimizer)
    print(f'Epoch {epoch + 1}, Loss: {loss.numpy():.4f}')

# 核心思想: 从随机潜在向量生成新样本
num_samples = 16
random_vector = tf.random.normal(shape=[num_samples, latent_dim])
generated_images = vae.decode(random_vector)

print("Generated images shape:", generated_images.shape)
print("Sample generated image min and max values:")
print(tf.reduce_min(generated_images), tf.reduce_max(generated_images))
