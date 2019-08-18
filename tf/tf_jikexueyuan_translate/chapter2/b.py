#!/usr/bin/env python
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])

#w = tf.Variable(tf.zeros([784, 10]))
w = tf.Variable(tf.truncated_normal([784,10], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None))
#b = tf.Variable(tf.zeros([10]))
b = tf.Variable(tf.truncated_normal([10], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None))
pred = tf.nn.softmax(tf.matmul(x,w)+b)
loss = tf.reduce_mean(tf.square(pred-y))
#loss = tf.reduce_sum(tf.square(pred-y))
#loss = -tf.reduce_sum(y*tf.log(pred+0.01))
train_op = tf.train.GradientDescentOptimizer(learning_rate=1).minimize(loss)

def print_tensor(te):
    print te
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        print sess.run(te)

correct_pred = tf.equal(tf.argmax(pred, axis=1), tf.argmax(y, axis=1))
acc = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    for i in range(10000):
        batch_xs, batch_ys = mnist.train.next_batch(1000)
        pred_sum = tf.reduce_sum(pred)
        sess.run([train_op, loss, pred_sum], feed_dict={x:batch_xs,y:batch_ys})
        #sess.run([train_op], feed_dict={x:mnist.train.images,y:mnist.train.labels})

        if i%1000==0:
            print sess.run([acc, loss], feed_dict={x:mnist.train.images,y:mnist.train.labels})
