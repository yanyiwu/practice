import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class POSO(keras.Model):
    def __init__(self, num_features, num_modules, hidden_dim, output_dim):
        super(POSO, self).__init__()
        self.num_modules = num_modules
        
        # Gate network
        self.gate = layers.Dense(num_modules, activation='softmax')
        
        # Expert modules
        self.modules = [
            keras.Sequential([
                layers.Dense(hidden_dim, activation='relu'),
                layers.Dense(output_dim)
            ]) for _ in range(num_modules)
        ]
        
        # User feature embedding
        self.user_embedding = layers.Embedding(num_features, hidden_dim)
        # num_features: 1000
        # hidden_dim: 64
        
        # Add a dense layer for user features
        self.user_dense = layers.Dense(hidden_dim)
        
    def call(self, inputs):
        user_features, item_features = inputs
        # user_features shape: (batch_size, num_features)
        # user_features shape: (32, 10)
        # item_features shape: (batch_size, item_feature_dim)   
        # item_features shape: (32, 20)
        
        # Get user embedding
        user_embed = self.user_embedding(user_features)
        # user_embed shape: (32, num_user_features, 64)
        
        user_embed = tf.reduce_mean(user_embed, axis=1)
        # user_embed shape: (32, 64)
        
        # Process user features through dense layer
        user_features_processed = self.user_dense(tf.cast(user_features, tf.float32))
        # user_features_processed shape: (batch_size, hidden_dim)
        # user_features_processed shape: (32, 64)
        
        # Calculate gate weights
        gate_weights = self.gate(tf.concat([user_embed, user_features_processed], axis=1))
        # gate_weights shape: (batch_size, num_modules)
        # gate_weights shape: (32, 5)
        
        # Output of each module
        module_outputs = [module(item_features) for module in self.modules]
        # module_outputs 是一个列表，长度为 5
        # 每个元素的形状是 (32, 1)
        
        # Weighted combination of module outputs
        final_output = tf.stack(module_outputs, axis=1) 
        # final_output shape: (32, 5, 1)
        
        final_output = tf.reduce_sum(final_output * tf.expand_dims(gate_weights, -1), axis=1)
        # final_output shape: (32, 1)
        
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






