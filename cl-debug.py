import tensorflow as tf
import numpy as np

class ContrastiveLearning(tf.keras.Model):
    def __init__(self, encoder, projection_dim=128, temperature=0.5):
        super(ContrastiveLearning, self).__init__()
        self.encoder = encoder
        self.projector = tf.keras.Sequential([
            tf.keras.layers.Dense(projection_dim, activation='relu'),
            tf.keras.layers.Dense(projection_dim)
        ])
        # self.projector.output_shape: [batch_size, projection_dim] 
        self.temperature = temperature

    def call(self, inputs):
        x1, x2 = inputs
        # 核心思想1: 对同一图像的两个增强版本进行编码
        # 目标是让模型学习到图像的不变特征，而忽略增强带来的差异
        z1 = self.projector(self.encoder(x1))
        z2 = self.projector(self.encoder(x2))
        return z1, z2

    def contrastive_loss(self, z1, z2):
        # 核心思想2: 最大化同一图像不同视图的相似度，最小化不同图像视图的相似度
        z1 = tf.math.l2_normalize(z1, axis=1)
        z2 = tf.math.l2_normalize(z2, axis=1)
        
        # 计算批次内所有样本对之间的相似度
        similarity_matrix = tf.matmul(z1, z2, transpose_b=True) / self.temperature
        # similarity_matrix shape: [batch_size, batch_size] 
        # similarity_matrix 中，对角线元素是正样本对
        # 非对角线元素自动成为负样本对
        
        batch_size = tf.shape(z1)[0]
        contrastive_labels = tf.range(batch_size)
        
        # 核心思想3: 将问题转化为分类任务
        # 对角线元素（正样本对）应该有最大的相似度
        # 非对角线元素（负样本对）应该有较小的相似度
        loss = tf.keras.losses.sparse_categorical_crossentropy(
            contrastive_labels, similarity_matrix, from_logits=True
        )
        # loss shape: [batch_size]  
        return tf.reduce_mean(loss)

# 核心思想4: 无监督学习
# 通过数据增强创建正样本对，不需要人工标注
# 模型通过对比学习自动学习有用的特征表示，可用于下游任务

# Example usage
encoder = tf.keras.applications.ResNet50(include_top=False, weights=None, pooling='avg')
# encoder.output_shape: [batch_size, 2048]  

cl_model = ContrastiveLearning(encoder)

# Create some dummy data
batch_size = 32
x1 = tf.random.normal((batch_size, 224, 224, 3))
x2 = tf.random.normal((batch_size, 224, 224, 3))

# Define the optimizer
optimizer = tf.keras.optimizers.Adam()

# Training step
@tf.function
def train_step(x1, x2):
    with tf.GradientTape() as tape:
        z1, z2 = cl_model((x1, x2))
        loss = cl_model.contrastive_loss(z1, z2)

    gradients = tape.gradient(loss, cl_model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, cl_model.trainable_variables))
    return loss

# Perform a single training step
loss = train_step(x1, x2)
print(f"Loss: {loss.numpy()}")
