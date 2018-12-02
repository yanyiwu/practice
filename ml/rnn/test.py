#!/usr/bin/python
#-*- encoding: utf8
# from: https://zhuanlan.zhihu.com/p/31786131
import numpy as np

def sigmoid(x):
    return 1.0 / (1.0+np.exp(-x))
# sigmoid导数
def sigmoid_derivative(output):
    return output * (1.0 - output)

int2binary = {}
binary_dim = 8
largest_number = pow(2,binary_dim)

binary = np.unpackbits(np.array([range(largest_number)], dtype=np.uint8).T,
                                             axis=1)

for i in range(largest_number):
    int2binary[i] = binary[i]

# 模型参数
input_dim = 2
hidden_dim = 16
output_dim = 1
learing_rate = 1e-1


# 初始化模型参数
# 模型: h(t) = sigmoid(dot(X,U) + dot(V, h(t-1))) -> output(t) = sigmoid(dot(W, h(t)))
U = np.random.randn(input_dim, hidden_dim)
V = np.random.randn(hidden_dim, hidden_dim)
W = np.random.randn(hidden_dim, output_dim)

# 初始化参数梯度
dU = np.zeros_like(U)
dV = np.zeros_like(V)
dW = np.zeros_like(W)

#iterations = 1
iterations = 20000

# 训练过程：不使用batch
for i in range(iterations):
    # 生成一个简单的加法问题 （a+b = c), a, b 除以2防止c溢出
    a_int = np.random.randint(largest_number / 2)
    a = int2binary[a_int]
    b_int = np.random.randint(largest_number / 2)
    b = int2binary[b_int]

    c_int = a_int + b_int
    c = int2binary[c_int]
    d = np.zeros_like(c)
    #print a_int
    #print bin(a_int)
    #print a
    #print b
    #print c
    # 训练样本
    X = np.array([a, b]).T
    y = np.array([c]).T
    #print X
    #print y
    loss = 0  # 损失函数

    hs = [np.zeros((1, hidden_dim))]  # 保存每个时间步长下的隐含特征
    #print hs[0].shape
    os = []  # 保存每个时间步长的预测值
    # forward过程
    for t in reversed(range(binary_dim)):
        # 当前时刻特征
        xt = X[t]
        yt = y[t]
        #print t
        ht = sigmoid(xt.dot(U)+hs[-1].dot(V))
        ot = sigmoid(ht.dot(W))
        hs.append(ht)
        os.append(ot)
        loss += np.abs(ot-yt)[0][0]
        d[t]=np.round(ot)[0][0]
    #print d
    # backward过程
    future_d_ht = np.zeros((1, hidden_dim))  # 从上一个时刻传递的梯度
    for t in reversed(range(binary_dim)):
        #xt = X[binary_dim - t - 1].reshape(1, -1)
        #print 1,X[binary_dim - t - 1].shape
        #print 2,X[binary_dim - t - 1].reshape(1, -1).shape
        #print 2,X[binary_dim - t - 1].T.shape
        #print 'xxxx',t
        #print X[binary_dim - t - 1]
        #print X[binary_dim - t - 1].shape
        #print X[binary_dim - t - 1].reshape(1, -1)
        #print X[binary_dim - t - 1].reshape(1, -1).shape
        #print X[binary_dim - t - 1].reshape(1, -1).T
        #print X[binary_dim - t - 1].reshape(1, -1).T.shape

        xt = X[binary_dim - t - 1].reshape(1, -1)
        ht = hs[t+1]
        ht_prev = hs[t]
        ot = os[t]
        # d_loss/d_ot
        d_ot = ot - y[binary_dim - t - 1]
        d_ot_output = sigmoid_derivative(ot) * d_ot
	dW += ht.T.dot(d_ot_output)
        d_ht = d_ot_output.dot(W.T) + future_d_ht  # 别忘来了上一时刻传入的梯度
        d_ht_output = sigmoid_derivative(ht) * d_ht
        dU += xt.T.dot(d_ht_output)
        dV += ht_prev.T.dot(d_ht_output)

        # 更新future_d_ht
        future_d_ht = d_ht_output.dot(V.T)

    # SGD更新参数
    U -= learing_rate * dU
    V -= learing_rate * dV
    W -= learing_rate * dW

    # 重置梯度
    dU *= 0
    dV *= 0
    dW *= 0

    # 输出loss和预测结果
    if (i % 1000 == 0):
        print("loss:" + str(loss))
        print("Pred:" + str(d))
        print("True:" + str(c))
        out = 0
        for index, x in enumerate(reversed(d)):
            out += x * pow(2, index)
        print(str(a_int) + " + " + str(b_int) + " = " + str(out))
        print("------------")
