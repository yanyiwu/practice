#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf


features = {
    'sales' : [[5], [10], [8], [9]],
    #'sales' : [5, 10, 8, 9],
    'department': ['sports', 'sports', 'gardening', 'gardening']}

department_column = tf.feature_column.categorical_column_with_vocabulary_list(
        'department', ['sports', 'gardening'])
department_column = tf.feature_column.indicator_column(department_column)

columns = [
    tf.feature_column.numeric_column('sales'),
    department_column
]

inputs = tf.feature_column.input_layer(features, columns)
print("====")
print(inputs)
print(columns)
print("====")


var_init = tf.global_variables_initializer()
table_init = tf.tables_initializer()
sess = tf.Session()
print(sess.run((var_init, table_init)))

print(sess.run(inputs))
#print(len(sess.run(inputs)[0]))
