#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf


def conv_relu(input, kernel_shape, bias_shape):
    # Create variable named "weights".
    weights = tf.get_variable("weights", kernel_shape,
        initializer=tf.random_normal_initializer())
    # Create variable named "biases".
    biases = tf.get_variable("biases", bias_shape,
        initializer=tf.constant_initializer(0.0))
    conv = tf.nn.conv2d(input, weights,
        strides=[1, 1, 1, 1], padding='SAME')
    return tf.nn.relu(conv + biases)

#input1 = tf.random_normal([1,10,10,32])
#input2 = tf.random_normal([1,20,20,32])
#x = conv_relu(input1, kernel_shape=[5, 5, 32, 32], bias_shape=[32])
#x = conv_relu(x, kernel_shape=[5, 5, 32, 32], bias_shape = [32])  # This fails.
# failed


# Print all of the operations in the default graph.
g = tf.get_default_graph()
print(g.get_operations())
