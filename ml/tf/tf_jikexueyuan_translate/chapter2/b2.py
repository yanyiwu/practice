#!/usr/bin/env python
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import time,sys
def print_progress(epoches, step, start_ts):
    step = step + 1
    time_elapse = int(time.time()-start_ts)
    #interval_seconds = 5
    #if time_elapse % interval_seconds + 1 == interval_seconds:
    progress_percent = 100.0 *step/epoches
    time_left_minutes = (1.0*time_elapse/(progress_percent/100.0+1e-08)-time_elapse)/60.0
    print 'progress: %s%%, time elapse %s seconds, approximately %s minutes to be finished' %(progress_percent, time_elapse, time_left_minutes)

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
optimizer = tf.train.AdamOptimizer()
grads = optimizer.compute_gradients(loss)
train_op = optimizer.apply_gradients(grads)
for grad in grads:
    print grad
    g,v = grad
    name = v.name
    tf.summary.scalar('grad_abs_sum_%s' %(name), tf.reduce_sum(tf.abs(g)))

correct_pred = tf.equal(tf.argmax(pred, axis=1), tf.argmax(y, axis=1))
acc = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
tf.summary.scalar('acc', acc)
tf.summary.scalar('loss', loss)
summary_op = tf.summary.merge_all()
with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    logdir=sys.argv[0]+'.debug'
    writer = tf.summary.FileWriter(logdir, sess.graph)
    sess.run(init_op)
    epoches = 100000
    start_time = time.time()
    for i in range(epoches):
        batch_xs, batch_ys = mnist.train.next_batch(1000)
        pred_sum = tf.reduce_sum(pred)
        sess.run([train_op, loss, pred_sum], feed_dict={x:batch_xs,y:batch_ys})

        if i%100==0:
            summary_str = sess.run(summary_op, feed_dict={x:batch_xs, y: batch_ys})
            writer.add_summary(summary_str, i)
            writer.flush()
            print_progress(epoches, i, start_time)
