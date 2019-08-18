#!/usr/bin/env python
import sys
import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

#Please use alternatives such as official/mnist/dataset.py from tensorflow/models. 

