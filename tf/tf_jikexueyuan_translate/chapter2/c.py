#!/usr/bin/env python
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])
t = tf.reshape(x, [-1, 28, 28, 1], name='r1')

#conv1
w = tf.Variable(tf.truncated_normal([5,5,1,32], stddev=0.1))
b = tf.Variable(tf.constant(0.1, shape=[32]))
t = tf.nn.conv2d(t, w, strides=[1,1,1,1], padding='SAME')
t = tf.nn.relu(t + b)
t = tf.nn.max_pool(t, ksize=[1,2,2,1],strides=[1,2,2,1], padding='SAME')

#conv2
w = tf.Variable(tf.truncated_normal([5,5,32,64], stddev=0.1))
b = tf.Variable(tf.constant(0.1, shape=[64]))
t = tf.nn.conv2d(t, w, strides=[1,1,1,1], padding='SAME')
t = tf.nn.relu(t + b)
t = tf.nn.max_pool(t, ksize=[1,2,2,1],strides=[1,2,2,1], padding='SAME')

# fc dims
fc_dims=7*7*64
t = tf.reshape(t, [-1, fc_dims],name='r2')

fc_w = tf.Variable(tf.truncated_normal([fc_dims, 10], stddev=0.1))
fc_b = tf.Variable(tf.constant(0.1,shape=[10]))
pred = tf.nn.softmax(tf.matmul(t, fc_w) + fc_b)
#loss=-tf.reduce_sum(y*tf.log(pred))
loss=tf.reduce_sum(tf.square(pred-y))
#train_op = tf.train.GradientDescentOptimizer(learning_rate=10.0).minimize(loss)
#train_op = tf.train.AdamOptimizer().minimize(loss)
#train_op = tf.train.MomentumOptimizer(0.1,0.9).minimize(loss)
#train_op = tf.train.RMSPropOptimizer(0.0001).minimize(loss)
train_op = tf.train.GradientDescentOptimizer(learning_rate=1e-04).minimize(loss)

init_op = tf.global_variables_initializer()

acc_op = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(pred, axis=1), tf.argmax(y, axis=1)), tf.float32))

with tf.Session() as sess:
    sess.run(init_op)
    for i in range(20000):
        batch_xs, batch_ys = mnist.train.next_batch(50)
        sess.run([train_op], feed_dict={x:batch_xs, y:batch_ys})
        if i % 100 == 0:
            #print sess.run([acc_op,loss], feed_dict={x:batch_xs,y:batch_ys})
            print sess.run([acc_op,loss], feed_dict={x: mnist.test.images, y: mnist.test.labels})
