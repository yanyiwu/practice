#!/usr/bin/env python
import tensorflow as tf
import numpy as np

x_data = np.float32(np.random.rand(2,100))
y_data = np.dot([0.1,0.2], x_data) + 0.3

b = tf.Variable(tf.zeros([1]))
W = tf.Variable(tf.random_uniform([1,2]))
print W
y = tf.matmul(W, x_data) + b

loss = tf.reduce_mean(tf.square(y-y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

for step in xrange(0,200):
    sess.run(train)
    print step, sess.run(W), sess.run(b), sess.run(loss)
