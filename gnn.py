
import tensorflow as tf
from tensorflow import keras
import numpy as np

# 定义图神经网络层
class GraphConvLayer(keras.layers.Layer):
    def __init__(self, units, activation=None):
        super(GraphConvLayer, self).__init__()
        self.units = units
        self.activation = activation

    def build(self, input_shape):
        self.weight = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer='glorot_uniform',
            name='weight'
        )
        self.bias = self.add_weight(
            shape=(self.units,),
            initializer='zeros',
            name='bias'
        )

    def call(self, inputs, adj_matrix):
        # 图卷积操作: H = σ(AXW + b)
        # A: 邻接矩阵, X: 节点特征, W: 权重矩阵, b: 偏置
        support = tf.matmul(inputs, self.weight)
        output = tf.matmul(adj_matrix, support)
        output = output + self.bias
        return self.activation(output) if self.activation else output

# 创建GNN模型
class GNNModel(keras.Model):
    def __init__(self, num_classes):
        super(GNNModel, self).__init__()
        self.gc1 = GraphConvLayer(16, activation=tf.nn.relu)
        self.gc2 = GraphConvLayer(num_classes)
        self.dropout = keras.layers.Dropout(0.5)

    def call(self, inputs, adj_matrix, training=False):
        x = self.gc1(inputs, adj_matrix)
        x = self.dropout(x, training=training)
        return self.gc2(x, adj_matrix)

# 生成示例数据
num_nodes = 100
num_features = 10
num_classes = 7

# 随机生成节点特征和邻接矩阵
node_features = np.random.randn(num_nodes, num_features).astype(np.float32)
adj_matrix = np.random.randint(0, 2, (num_nodes, num_nodes)).astype(np.float32)
labels = np.random.randint(0, num_classes, num_nodes)

# 创建和编译模型
model = GNNModel(num_classes)
optimizer = keras.optimizers.Adam(learning_rate=0.01)
loss_fn = keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# 训练模型
@tf.function
def train_step(features, adj, labels):
    with tf.GradientTape() as tape:
        predictions = model(features, adj, training=True)
        loss = loss_fn(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss

# 训练循环
for epoch in range(200):
    loss = train_step(node_features, adj_matrix, labels)
    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.numpy():.4f}")

# 评估模型
predictions = model(node_features, adj_matrix, training=False)
accuracy = np.mean(np.argmax(predictions, axis=1) == labels)
print(f"Final accuracy: {accuracy:.4f}")

# 原理解释：
# 1. GraphConvLayer实现了图卷积操作，即H = σ(AXW + b)，其中A是邻接矩阵，X是节点特征。
# 2. GNNModel包含两个GraphConvLayer，形成一个两层的GNN。
# 3. 在每个训练步骤中，模型接收节点特征和邻接矩阵作为输入，通过图卷积层传播信息。
# 4. 损失函数使用稀疏分类交叉熵，优化器使用Adam。
# 5. 训练过程中，模型学习如何聚合邻居信息来更新节点表示，从而完成节点分类任务。
