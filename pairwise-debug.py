import tensorflow as tf
import numpy as np

# 生成一些示例数据
def generate_data(num_queries, num_docs_per_query, feature_dim):
    X = np.random.rand(num_queries, num_docs_per_query, feature_dim)
    y = np.random.randint(0, 2, (num_queries, num_docs_per_query))
    return X, y

# 定义 PairWise 模型
class PairWiseModel(tf.keras.Model):
    def __init__(self, hidden_units):
        super(PairWiseModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(hidden_units, activation='relu')
        self.dense2 = tf.keras.layers.Dense(1)

    def call(self, inputs):
        x = self.dense1(inputs)
        return self.dense2(x)

# 定义 PairWise 损失函数
def pairwise_loss(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    diff = y_pred[:, 0] - y_pred[:, 1]
    return -tf.reduce_mean(tf.math.log(tf.nn.sigmoid(diff)))

# 主函数
def main():
    # 生成数据
    X_train, y_train = generate_data(1000, 2, 5)
    X_test, y_test = generate_data(100, 2, 5)

    # 创建模型
    model = PairWiseModel(64)
    model.compile(optimizer='adam', loss=pairwise_loss)

    # 训练模型
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

    # 评估模型
    test_loss = model.evaluate(X_test, y_test)
    print(f"Test loss: {test_loss}")

    # 使用模型进行预测
    predictions = model.predict(X_test[:5])
    print("Sample predictions shape:", predictions.shape)
    print("Sample predictions:")
    print(predictions)

if __name__ == "__main__":
    main()
