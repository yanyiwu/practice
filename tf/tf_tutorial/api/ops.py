#!/usr/bin/env python
import tensorflow as tf

tf.enable_eager_execution()

a1 = tf.random_normal([4,4], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
a2 = tf.random_normal([4,4], mean=0.0, stddev=1.0, dtype=tf.float32)
print a1
print a2
print tf.add_n([a1,a2])
