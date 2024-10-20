import tensorflow as tf
import numpy as np
from tensorflow.keras import layers

# 定义 Diffusion 模型
class DiffusionModel(tf.keras.Model):
    def __init__(self, img_size, num_steps):
        super(DiffusionModel, self).__init__()
        self.img_size = img_size
        self.num_steps = num_steps

        self.model = tf.keras.Sequential([
            layers.Conv2D(32, 3, activation='relu', padding='same'),
            # model shape: (32, 32, 32, 103) -> (32, 32, 32, 32)  

            layers.Conv2D(64, 3, activation='relu', padding='same'),
            # model shape: (32, 32, 32, 32) -> (32, 32, 32, 64)

            layers.Conv2D(64, 3, activation='relu', padding='same'),
            # model shape: (32, 32, 32, 64) -> (32, 32, 32, 64)

            layers.Conv2D(32, 3, activation='relu', padding='same'),
            # model shape: (32, 32, 32, 64) -> (32, 32, 32, 32)

            layers.Conv2D(3, 3, padding='same')
            # model shape: (32, 32, 32, 32) -> (32, 32, 32, 3)  
        ])
        # model shape: (32, 32, 32, 103) -> (32, 32, 32, 3) 

    def call(self, inputs):
        x, t = inputs
        # x shape: (32, 32, 32, 3)
        # t shape: (32,)    
        t = tf.cast(t, dtype=tf.int32)
        # t shape: (32,)
        t_emb = tf.one_hot(t, self.num_steps)
        # t_emb shape: (32, 100)
        t_emb = tf.repeat(t_emb, repeats=self.img_size*self.img_size)
        # t_emb shape: [3276800]
        t_emb = tf.reshape(t_emb, (-1, self.img_size, self.img_size, self.num_steps))
        # t_emb shape: (32, 32, 32, 100)
        x_t = tf.concat([x, t_emb], axis=-1)
        # x_t shape: (32, 32, 32, 103)
        r = self.model(x_t)
        # r shape: (32, 32, 32, 3)  
        return r

# 添加噪声函数
def add_noise(images, noise_factor):
    noise = tf.random.normal(shape=tf.shape(images), mean=0.0, stddev=1.0)
    # noise shape: (32, 32, 32, 3)
    noisy_images = images + noise_factor * noise
    # noisy_images shape: (32, 32, 32, 3)
    return tf.clip_by_value(noisy_images, 0.0, 1.0)

# 主函数
def main():
    # 设置参数
    img_size = 32
    num_steps = 100
    batch_size = 32

    # 创建模型
    model = DiffusionModel(img_size, num_steps)
    model.compile(optimizer='adam', loss='mse')

    # 生成示例数据
    X = tf.random.uniform((batch_size, img_size, img_size, 3))
    # X shape: (32, 32, 32, 3)
    
    # 训练循环
    for epoch in range(10):
        for step in range(num_steps):
            t = tf.ones((batch_size,)) * step
            # t shape: (32,)    
            noise_factor = step / num_steps
            noisy_X = add_noise(X, noise_factor)
            # noisy_X shape: (32, 32, 32, 3)
            loss = model.train_on_batch([noisy_X, t], X)
            print(f"Epoch {epoch+1}, Loss: {loss}")

    # 使用模型进行去噪
    test_X = tf.random.uniform((1, img_size, img_size, 3))
    noisy_test_X = add_noise(test_X, 0.5)
    
    for step in reversed(range(num_steps)):
        t = tf.ones((1,)) * step
        prediction = model([noisy_test_X, t])
        noisy_test_X = prediction

    print("Sample prediction shape:", prediction.shape)
    print("Sample prediction min and max values:")
    print(tf.reduce_min(prediction), tf.reduce_max(prediction))

if __name__ == "__main__":
    main()
