import tensorflow as tf
import numpy as np
from tensorflow.keras import layers

# 定义 DIT (Diffusion Image Transformer) 模型
class DITModel(tf.keras.Model):
    def __init__(self, img_size, patch_size, num_patches, d_model, num_heads, dff, num_layers):
        super(DITModel, self).__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = num_patches

        self.patch_embed = layers.Conv2D(d_model, kernel_size=patch_size, strides=patch_size)
        self.pos_embed = layers.Embedding(num_patches, d_model)
        
        self.transformer_layers = [
            layers.TransformerEncoderLayer(num_heads, d_model, dff)
            for _ in range(num_layers)
        ]
        
        self.final_layer = layers.Dense(patch_size * patch_size * 3)  # 3 for RGB channels

    def call(self, inputs, t):
        # inputs shape: (batch_size, img_size, img_size, 3)
        # t shape: (batch_size,)
        
        x = self.patch_embed(inputs)
        _, h, w, c = x.shape
        x = tf.reshape(x, (-1, h * w, c))
        
        positions = tf.range(start=0, limit=self.num_patches, delta=1)
        pos_embed = self.pos_embed(positions)
        x = x + pos_embed
        
        t = tf.expand_dims(t, axis=1)
        t = tf.tile(t, [1, h * w])
        t = tf.expand_dims(t, axis=-1)
        x = tf.concat([x, t], axis=-1)
        
        for layer in self.transformer_layers:
            x = layer(x)
        
        x = self.final_layer(x)
        x = tf.reshape(x, (-1, self.img_size, self.img_size, 3))
        return x

# 生成噪声图像
def add_noise(images, noise_factor):
    noise = tf.random.normal(shape=tf.shape(images), mean=0.0, stddev=1.0)
    noisy_images = images + noise_factor * noise
    return tf.clip_by_value(noisy_images, 0.0, 1.0)

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
    
    # 编译模型
    model.compile(optimizer='adam', loss='mse')
    
    # 生成示例数据
    batch_size = 32
    X = tf.random.uniform((batch_size, img_size, img_size, 3))
    t = tf.random.uniform((batch_size,), maxval=1.0)
    y = add_noise(X, 0.1)  # 添加轻微噪声作为目标
    
    # 训练模型
    model.fit([X, t], y, epochs=10, batch_size=32)
    
    # 使用模型进行预测
    test_X = tf.random.uniform((1, img_size, img_size, 3))
    test_t = tf.constant([0.5])
    prediction = model([test_X, test_t])
    
    print("Sample prediction shape:", prediction.shape)
    print("Sample prediction min and max values:")
    print(tf.reduce_min(prediction), tf.reduce_max(prediction))

if __name__ == "__main__":
    main()

