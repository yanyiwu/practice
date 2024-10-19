import tensorflow as tf
import numpy as np

# Pairwise: 生成数据函数固定每个查询有2个文档
# Listwise: 每个查询可以有多个文档
# Pointwise: 每个样本是单个文档
def generate_data(num_queries, num_docs_per_query, feature_dim):
    # Pairwise: num_docs_per_query 固定为 2
    # Listwise: num_docs_per_query 可以大于 2
    # Pointwise: 不需要 num_docs_per_query 参数
    X = np.random.rand(num_queries, num_docs_per_query, feature_dim)
    # Pairwise: y 表示第一个文档是否应该排在第二个文档之前
    # Listwise: y 可能是每个文档的相关性分数
    # Pointwise: y 是单个文档的相关性分数
    y = np.random.randint(0, 2, (num_queries, 1))
    return X, y

# Pairwise: 模型结构设计用于比较两个文档
# Listwise: 模型可能需要考虑所有文档
# Pointwise: 模型只处理单个文档
class PairwiseModel(tf.keras.Model):
    def __init__(self, hidden_units):
        super(PairwiseModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(hidden_units, activation='relu')
        # Pairwise: 最后一层输出单一分数，表示相对顺序
        # Listwise: 最后一层可能输出多个分数
        # Pointwise: 最后一层输出单个文档的分数
        self.dense2 = tf.keras.layers.Dense(1)

    def call(self, inputs):
        # Pairwise: 输入是一对文档
        # Listwise: 输入是多个文档
        # Pointwise: 输入是单个文档
        doc1, doc2 = inputs[:, 0, :], inputs[:, 1, :]
        feat1 = self.dense1(doc1)
        feat2 = self.dense1(doc2)
        # Pairwise: 比较两个文档的特征
        diff = feat1 - feat2
        return self.dense2(diff)

# Pairwise: 损失函数设计用于优化文档对的相对顺序
# Listwise: 损失函数考虑整个文档列表
# Pointwise: 损失函数针对单个文档的预测
def pairwise_loss(y_true, y_pred):
    return tf.keras.losses.binary_crossentropy(y_true, tf.sigmoid(y_pred))

# 主函数
def main():
    # Pairwise: 固定每个查询有2个文档
    # Listwise: 可以有多个文档
    # Pointwise: 每个样本是单个文档
    X_train, y_train = generate_data(1000, 2, 5)
    X_test, y_test = generate_data(100, 2, 5)

    # 创建模型
    model = PairwiseModel(64)
    model.compile(optimizer='adam', loss=pairwise_loss)

    # Pairwise: 训练数据是文档对
    # Listwise: 训练数据是完整的文档列表
    # Pointwise: 训练数据是独立的文档
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

    # 评估模型
    test_loss = model.evaluate(X_test, y_test)
    print(f"Test loss: {test_loss}")

    # Pairwise: 预测结果表示文档对的相对顺序
    # Listwise: 预测结果可能是整个列表的排序
    # Pointwise: 预测结果是单个文档的分数
    predictions = model.predict(X_test[:5])
    print("Sample predictions:", predictions)

if __name__ == "__main__":
    main()
