#!/usr/bin/env python
import tensorflow as tf

#k = tf.placeholder(tf.float32)

# Make a normal distribution, with a shifting mean
mean_moving_normal = tf.random_normal(shape=[10], mean=0.0, stddev=1)
# Record that distribution into a histogram summary
tf.summary.histogram("normal/moving_mean", mean_moving_normal)

sess = tf.Session()
# Setup a session and summary writer
writer = tf.summary.FileWriter("./h2")
summaries = tf.summary.merge_all()
summ = sess.run(summaries)
writer.add_summary(summ, global_step=0)
