#!/usr/local/bin/python
#-*-coding:utf8
import tensorflow as tf
print(tf.__version__)
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
imdb = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

