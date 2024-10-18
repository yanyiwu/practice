import tensorflow as tf
import numpy as np

# Pairwise: 生成数据函数固定每个查询只有2个文档
# Listwise: 每个查询可以有多个文档
def generate_data(num_queries, num_docs_per_query, feature_dim):
    # Pairwise: num_docs_per_query 固定为 2
    # Listwise: num_docs_per_query 可以是任意大于1的整数
    X = np.random.rand(num_queries, num_docs_per_query, feature_dim)
    # Pairwise: y 表示第一个文档是否应该排在第二个文档之前
    # Listwise: y 通常是每个文档的相关性分数
    y = np.random.randint(0, 2, (num_queries, 1))
    return X, y

# Pairwise: 模型结构设计为比较两个文档
# Listwise: 模型需要处理可变数量的文档
class PairWiseModel(tf.keras.Model):
    def __init__(self, hidden_units):
        super(PairWiseModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(hidden_units, activation='relu')
        # Pairwise: 最后一层输出单一分数，表示相对顺序
        # Listwise: 最后一层通常为每个文档输出一个分数
        self.dense2 = tf.keras.layers.Dense(1)

    def call(self, inputs):
        # Pairwise: 处理固定的两个文档
        # Listwise: 需要处理可变数量的文档
        doc1 = self.dense1(inputs[:, 0, :])
        doc2 = self.dense1(inputs[:, 1, :])
        combined = tf.concat([doc1, doc2], axis=1)
        return self.dense2(combined)

# Pairwise: 损失函数设计为优化文档对的相对顺序
# Listwise: 损失函数考虑整个文档列表的排序
def pairwise_loss(y_true, y_pred):
    # Pairwise: 使用 binary crossentropy 或 hinge loss
    # Listwise: 通常使用特殊的排序损失函数，如 ListMLE
    return tf.keras.losses.binary_crossentropy(y_true, y_pred)

# 主函数
def main():
    # Pairwise: 固定为2个文档
    # Listwise: 可以有多个文档
    X_train, y_train = generate_data(1000, 2, 5)
    X_test, y_test = generate_data(100, 2, 5)

    # 创建模型
    model = PairWiseModel(64)
    model.compile(optimizer='adam', loss=pairwise_loss)

    # Pairwise: 每个批次包含多个文档对
    # Listwise: 每个批次包含多个完整的文档列表
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

    # 评估模型
    test_loss = model.evaluate(X_test, y_test)
    print(f"Test loss: {test_loss}")

    # Pairwise: 预测结果是文档对的相对顺序
    # Listwise: 预测结果是整个文档列表的排序分数
    predictions = model.predict(X_test[:5])
    print("Sample predictions:", predictions)

if __name__ == "__main__":
    main()
