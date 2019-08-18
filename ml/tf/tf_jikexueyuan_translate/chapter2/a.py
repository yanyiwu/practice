#!/usr/bin/env python
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
import tensorflow as tf

x = tf.placeholder("float", [None, 784])
print x
W = tf.Variable(tf.zeros([784,10]))
print W
b = tf.Variable(tf.zeros([10]))
print b
t = tf.matmul(x, W)
print t
t = t+b
print t
y = tf.nn.softmax(t)

def print_tensor(te):
    print te
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        print sess.run(te)



# 2x2
# [1,2
#  3,4]
c1 = tf.constant([[1,2],[3,4]])
# 1x2
# [10,20]
c2 = tf.constant([10,20])
print_tensor(c1+c2)
c3 = tf.constant([10])
print_tensor(c1+c3)
