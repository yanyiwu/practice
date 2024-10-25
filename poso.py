import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class POSO(keras.Model):
    def __init__(self, num_features, num_modules, hidden_dim, output_dim):
        super(POSO, self).__init__()
        self.num_modules = num_modules
        
        # 门控网络
        self.gate = layers.Dense(num_modules, activation='softmax')
        
        # 多个专家模块
        self.modules = [
            keras.Sequential([
                layers.Dense(hidden_dim, activation='relu'),
                layers.Dense(output_dim)
            ]) for _ in range(num_modules)
        ]
        
        # 用户特征嵌入
        self.user_embedding = layers.Embedding(num_features, hidden_dim)
        
    def call(self, inputs):
        user_features, item_features = inputs
        
        # 获取用户嵌入
        user_embed = self.user_embedding(user_features)
        user_embed = tf.reduce_mean(user_embed, axis=1)
        
        # 计算门控权重
        gate_weights = self.gate(tf.concat([user_embed, user_features], axis=1))
        
        # 每个模块的输出
        module_outputs = [module(item_features) for module in self.modules]
        
        # 加权组合模块输出
        final_output = tf.stack(module_outputs, axis=1)
        final_output = tf.reduce_sum(final_output * tf.expand_dims(gate_weights, -1), axis=1)
        
        return final_output

# 创建和编译模型
num_features = 1000  # 用户特征数量
num_modules = 5  # 专家模块数量
hidden_dim = 64
output_dim = 1  # 对于二分类问题

model = POSO(num_features, num_modules, hidden_dim, output_dim)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 模拟数据
num_samples = 10000
user_features = tf.random.uniform((num_samples, 10), maxval=num_features, dtype=tf.int32)
item_features = tf.random.normal((num_samples, 20))
labels = tf.random.uniform((num_samples,), maxval=2, dtype=tf.int32)

# 训练模型
model.fit([user_features, item_features], labels, epochs=5, batch_size=32, validation_split=0.2)

# 评估模型
test_loss, test_acc = model.evaluate([user_features, item_features], labels, verbose=2)
print(f'\nTest accuracy: {test_acc}')





