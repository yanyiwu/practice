#!/usr/bin/env python
import tensorflow as tf

def print_tensor(te):
    print te
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        print sess.run(te)
    #print tf.summary(te)

print_tensor(tf.random_normal([4,4], mean=0.0, stddev=1.0, dtype=tf.float32, seed=None, name=None))
print_tensor(tf.random_normal([4,4], mean=0.0, stddev=1.0, dtype=tf.float32, seed=None, name='x'))
print_tensor(tf.random_normal([4,4], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None))
print_tensor(tf.random_normal([4,4], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None))
print_tensor(tf.truncated_normal([4,4], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None))

a1 = tf.random_normal([2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a1)
a2 = tf.random_normal([2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a2)
a3 = tf.concat([a1,a2], axis=0)
print_tensor(a3)

a1 = tf.random_normal([2,2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a1)
a2 = tf.random_normal([2,2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a2)
a3 = tf.concat([a1,a2], axis=0)
print_tensor(a3)
a3 = tf.concat([a1,a2], axis=1)
print_tensor(a3)
a4 = tf.reduce_sum(a3, axis=0)
print_tensor(a4)
a4 = tf.reduce_sum(a3, axis=1)
print_tensor(a4)
print_tensor(a1)
print_tensor(a1+a2)
print_tensor(tf.add(a1,a2))

print '======='
a1 = tf.random_normal([1,2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a1)
a2 = tf.random_normal([2,4], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a2)
print_tensor(tf.matmul(a1,a2))
print '======='
a1 = tf.random_normal([1,2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a1)
a2 = tf.random_normal([1,2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a2)
print_tensor(tf.multiply(a1,a2))
print '======='
a1 = tf.range(0,10)
print_tensor(a1)
print '======='
a1 = tf.constant(1, shape=[10])
print_tensor(a1)
print '======='
a1 = tf.gather(tf.range(0,10),[1,3,5])
print_tensor(a1)
print '======='
a1 = tf.random_normal([1,2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
a1 = tf.norm(a1)
print_tensor(a1)

print '======='
a1 = tf.gather(tf.range(0,10),[1,3,5])
print_tensor(a1)
print_tensor(tf.slice(a1, [1], [2]))

print '======='
a1 = tf.random_normal([2,2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a1)
print_tensor(tf.slice(a1, [0,0], [2,1]))
print_tensor(tf.slice(a1, [0,0], [-1,-1]))


print '======='
a1 = tf.random_normal([2,2], mean=0.0, stddev=1.0, dtype=tf.float32, seed=1, name=None)
print_tensor(a1)
print_tensor(tf.add_n([a1]))
print_tensor(tf.reduce_sum([a1]))

print '===='
import numpy as np
data = np.random.random((4, 3))
print data
