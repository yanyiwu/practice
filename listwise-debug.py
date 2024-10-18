import tensorflow as tf
import numpy as np

# 生成一些示例数据
def generate_data(num_queries, num_docs_per_query, feature_dim):
    X = np.random.rand(num_queries, num_docs_per_query, feature_dim)
    y = np.random.randint(0, 2, (num_queries, num_docs_per_query))
    y = np.expand_dims(y, axis=-1)  # 将 y 转换为 3D: (num_queries, num_docs_per_query, 1)
    return X, y

# 定义 ListWise 模型
class ListWiseModel(tf.keras.Model):
    def __init__(self, hidden_units):
        super(ListWiseModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(hidden_units, activation='relu')
        # 实际的 dense1 层形状: (hidden_units,)
        # 但应用于输入后的输出形状: (num_queries, num_docs_per_query, hidden_units)
        self.dense2 = tf.keras.layers.Dense(1)
        # 实际的 dense2 层形状: (1,)
        # 但应用于前一层输出后的输出形状: (num_queries, num_docs_per_query, 1)

    def call(self, inputs):
        # inputs shape: (num_queries, num_docs_per_query, feature_dim)
        x = self.dense1(inputs)
        # x shape: (num_queries, num_docs_per_query, hidden_units)
        return self.dense2(x)
        # output shape: (num_queries, num_docs_per_query, 1)

# 定义 ListWise 损失函数（这里使用简化版的 ListMLE）
def listwise_loss(y_true, y_pred):
    # 确保输入维度正确
    assert y_true.shape.ndims == 3, f"Expected y_true to be 3D, got shape {y_true.shape}"
    assert y_pred.shape.ndims == 3, f"Expected y_pred to be 3D, got shape {y_pred.shape}"
    
    # 移除最后一个维度，因为它现在是1
    y_true = tf.squeeze(y_true, axis=-1)
    # y_true shape: (num_queries, num_docs_per_query)   
    y_pred = tf.squeeze(y_pred, axis=-1)
    # y_pred shape: (num_queries, num_docs_per_query)

    sorted_indices = tf.argsort(y_true, direction='DESCENDING', axis=-1)
    sorted_pred = tf.gather(y_pred, sorted_indices, batch_dims=1)
    # sorted_pred shape: (num_queries, num_docs_per_query)
    loss = -tf.reduce_mean(tf.math.log_softmax(sorted_pred, axis=-1), axis=-1)
    # loss shape: (num_queries,)
    return loss

# 主函数
def main():
    # 生成数据
    X_train, y_train = generate_data(1000, 10, 5)
    # X_train shape: (1000, 10, 5)
    # y_train shape: (1000, 10, 1) 
    X_test, y_test = generate_data(100, 10, 5)
    # X_test shape: (100, 10, 5)
    # y_test shape: (100, 10, 1)

    # 创建模型
    model = ListWiseModel(64)
    model.compile(optimizer='adam', loss=listwise_loss)

    # 训练模型
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

    # 评估模型
    test_loss = model.evaluate(X_test, y_test)
    print(f"Test loss: {test_loss}")

    # 使用模型进行预测
    predictions = model.predict(X_test[:5])
    # predictions shape: (5, 10, 1) 
    print("Sample predictions shape:", predictions.shape)
    print("Sample predictions:")
    print(predictions)

if __name__ == "__main__":
    main()
