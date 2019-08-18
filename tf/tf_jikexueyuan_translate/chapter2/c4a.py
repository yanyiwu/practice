#!/usr/bin/env python
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import sys
import time

def print_progress(epoches, step, start_ts):
    step = step + 1
    time_elapse = int(time.time()-start_ts)
    #interval_seconds = 5
    #if time_elapse % interval_seconds + 1 == interval_seconds:
    progress_percent = 100.0 *step/epoches
    time_left_minutes = (1.0*time_elapse/(progress_percent/100.0+1e-08)-time_elapse)/60.0
    print 'progress: %s%%, time elapse %s seconds, approximately %s minutes to be finished' %(progress_percent, time_elapse, time_left_minutes)

def train(logdir, optimzer=tf.train.GradientDescentOptimizer(learning_rate=1e-04)):
    with tf.Graph().as_default():
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

        # fc dims
        fc_dims=14*14*32
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
        train_op = optimzer.minimize(loss)

        init_op = tf.global_variables_initializer()

        acc_op = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(pred, axis=1), tf.argmax(y, axis=1)), tf.float32))
        tf.summary.scalar('acc', acc_op)
        tf.summary.scalar('loss', loss)
        summary_op = tf.summary.merge_all()

        with tf.Session() as sess:
            writer = tf.summary.FileWriter(logdir, sess.graph)
            sess.run(init_op)

            start_time = time.time()
            epoches = 100*1000
            for i in range(epoches):
                batch_xs, batch_ys = mnist.train.next_batch(50)
                sess.run([train_op], feed_dict={x:batch_xs, y:batch_ys})
                #print summary_str
                step_interval = 1000
                if i % step_interval + 1 == step_interval:
                    #summary_str=sess.run(summary_op, feed_dict={x: mnist.test.images, y: mnist.test.labels})
                    summary_str=sess.run(summary_op, feed_dict={x: batch_xs, y: batch_ys})
                    writer.add_summary(summary_str, i)
                    writer.flush()
                    print_progress(epoches, i, start_time)
if __name__ == '__main__':
    train(logdir=sys.argv[0]+".sgd.1e-03", optimzer=tf.train.GradientDescentOptimizer(learning_rate=1e-03))
    train(logdir=sys.argv[0]+".sgd.1e-04", optimzer=tf.train.GradientDescentOptimizer(learning_rate=1e-04))
    train(logdir=sys.argv[0]+".sgd.1e-05", optimzer=tf.train.GradientDescentOptimizer(learning_rate=1e-05))
    train(logdir=sys.argv[0]+".sgd.1e-02", optimzer=tf.train.GradientDescentOptimizer(learning_rate=1e-02))
    train(logdir=sys.argv[0]+".sgd.1e-01", optimzer=tf.train.GradientDescentOptimizer(learning_rate=1e-01))
