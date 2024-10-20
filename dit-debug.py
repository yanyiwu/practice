import tensorflow as tf
import numpy as np
from tensorflow.keras import layers

class TransformerEncoderLayer(layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super(TransformerEncoderLayer, self).__init__()

        self.mha = layers.MultiHeadAttention(num_heads=num_heads, key_dim=d_model)
        self.ffn = tf.keras.Sequential([
            layers.Dense(dff, activation="relu"),
            layers.Dense(d_model)
        ])

        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)

        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, x, training):
        attn_output = self.mha(x, x, x)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(x + attn_output)

        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

# 定义 DIT (Diffusion Image Transformer) 模型
class DITModel(tf.keras.Model):
    def __init__(self, img_size, patch_size, num_patches, d_model, num_heads, dff, num_layers):
        super(DITModel, self).__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = num_patches
        self.d_model = d_model

        self.patch_embed = layers.Conv2D(d_model, kernel_size=patch_size, strides=patch_size)
        self.pos_embed = layers.Embedding(num_patches, d_model)
        
        self.transformer_layers = [
            TransformerEncoderLayer(d_model, num_heads, dff)
            for _ in range(num_layers)
        ]
        
        self.final_layer = layers.Dense(patch_size * patch_size * 3)  # 3 for RGB channels

    def build(self, input_shape):
        # 实现 build 方法来创建变量
        self.time_embed = self.add_weight(
            name="time_embed",
            shape=(1, 1, self.d_model),
            initializer="random_normal",
            trainable=True
        )
        super(DITModel, self).build(input_shape)

    def call(self, inputs, training=False):
        x, t = inputs
        # x shape: (batch_size, img_size, img_size, 3)
        # t shape: (batch_size,)
        
        x = self.patch_embed(x)
        _, h, w, c = x.shape
        x = tf.reshape(x, (-1, h * w, c))
        
        positions = tf.range(start=0, limit=self.num_patches, delta=1)
        pos_embed = self.pos_embed(positions)
        x = x + pos_embed
        
        # 使用广播将时间嵌入添加到所有patch
        t = tf.expand_dims(tf.expand_dims(t, -1), -1)  # (batch_size, 1, 1)
        time_embed = t * self.time_embed  # (batch_size, 1, d_model)
        x = x + time_embed
        
        for layer in self.transformer_layers:
            x = layer(x, training=training)
        
        x = self.final_layer(x)
        x = tf.reshape(x, (-1, self.img_size, self.img_size, 3))
        return x

# 生成噪声图像
def add_noise(images, t):
    noise = tf.random.normal(shape=tf.shape(images))
    alpha_t = 1 - diffusion_schedule(t)
    alpha_t = tf.reshape(alpha_t, (-1, 1, 1, 1))  # 调整形状以进行广播
    noisy_images = tf.sqrt(alpha_t) * images + tf.sqrt(1 - alpha_t) * noise
    return noisy_images, noise

def diffusion_schedule(t, start=0.0001, end=0.02):
    return start + t * (end - start)

# 更新 train_step 函数
@tf.function
def train_step(model, optimizer, images):
    batch_size = tf.shape(images)[0]
    t = tf.random.uniform((batch_size,), minval=0, maxval=1)
    
    noisy_images, noise = add_noise(images, t)
    
    with tf.GradientTape() as tape:
        predicted_noise = model([noisy_images, t], training=True)
        loss = tf.reduce_mean(tf.square(noise - predicted_noise))
    
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    
    return loss

# 更改 reverse_diffusion 函数
def reverse_diffusion(model, x, num_steps=100):
    for t in tf.linspace(1.0, 0.0, num_steps):
        t_batch = tf.ones((tf.shape(x)[0],)) * t
        predicted_noise = model([x, t_batch], training=False)
        x = (x - (1 - t) * predicted_noise) / tf.sqrt(t)
    return x

# 主函数
def main():
    # 设置参数
    img_size = 32
    patch_size = 4
    num_patches = (img_size // patch_size) ** 2
    d_model = 256
    num_heads = 8
    dff = 512
    num_layers = 6
    
    # 创建模型
    model = DITModel(img_size, patch_size, num_patches, d_model, num_heads, dff, num_layers)
    
    # 创建优化器
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
    
    # 生成示例数据
    batch_size = 32
    num_epochs = 1
    steps_per_epoch = 3
    
    # 编译模型
    model.compile(optimizer=optimizer, loss='mse')
    
    for epoch in range(num_epochs):
        for step in range(steps_per_epoch):
            # 在实际应用中，您应该从真实的数据集加载图像
            X = tf.random.uniform((batch_size, img_size, img_size, 3))
            loss = train_step(model, optimizer, X)
        
        print(f"Epoch {epoch + 1}, Loss: {loss.numpy():.4f}")
    
    # 使用模型进行预测
    test_X = tf.random.normal((1, img_size, img_size, 3))  # 从纯噪声开始
    prediction = reverse_diffusion(model, test_X)
    
    print("Sample prediction shape:", prediction.shape)
    print("Sample prediction min and max values:")
    print(tf.reduce_min(prediction), tf.reduce_max(prediction))

if __name__ == "__main__":
    main()
