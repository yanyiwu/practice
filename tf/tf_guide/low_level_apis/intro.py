#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf


a = tf.constant(3.0, dtype=tf.float32)
b = tf.constant(4.0) # also tf.float32 implicitly
total = a + b
print(a)
print(b)
print(total)


writer = tf.summary.FileWriter('.')
writer.add_graph(tf.get_default_graph())

sess = tf.Session()
print(sess.run(total))

print(sess.run({'ab':(a, b), 'total':total}))

vec = tf.random_uniform(shape=(3,))
out1 = vec + 1
out2 = vec + 2
print(sess.run(vec))
print(sess.run(vec))
print(sess.run((out1, out2)))

x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)
z = x + y

print(sess.run(z, feed_dict={z:1}))
print(sess.run(z, feed_dict={x: 3, y: 4.5}))
print(sess.run(z, feed_dict={x: [1, 3], y: [2, 4]}))


my_data = [
    [0, 1,],
    [2, 3,],
    [4, 5,],
    [6, 7,],
]
slices = tf.data.Dataset.from_tensor_slices(my_data)
print(slices)
next_item = slices.make_one_shot_iterator().get_next()
print(next_item)


while True:
  try:
    print(sess.run(next_item))
  except tf.errors.OutOfRangeError:
    break

r = tf.random_normal([10,3])
dataset = tf.data.Dataset.from_tensor_slices(r)
iterator = dataset.make_initializable_iterator()
next_row = iterator.get_next()

sess.run(iterator.initializer)
while True:
  try:
    print(sess.run(next_row))
  except tf.errors.OutOfRangeError:
    break


x = tf.placeholder(tf.float32, shape=[None, 3])
print(x)
linear_model = tf.layers.Dense(units=1)
print(linear_model)
y = linear_model(x)
print(y)

init = tf.global_variables_initializer()
print("====")
print(init)
print("====")
print(sess.run(init))
print("====")
print(sess.run(y, {x: [[1, 2, 3],[4, 5, 6]]}))

print("====")
x = tf.placeholder(tf.float32, shape=[None, 3])
y = tf.layers.dense(x, units=1)

init = tf.global_variables_initializer()
sess.run(init)

print(sess.run(y, {x: [[1, 2, 3], [4, 5, 6]]}))


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

x = tf.constant([[1], [2], [3], [4]], dtype=tf.float32)
y_true = tf.constant([[0], [-1], [-2], [-3]], dtype=tf.float32)


linear_model = tf.layers.Dense(units=1)
y_pred = linear_model(x)

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)

print(sess.run(y_pred))


loss = tf.losses.mean_squared_error(labels=y_true, predictions=y_pred)

print(sess.run(loss))

optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)


for i in range(100):
  train_val, loss_value = sess.run((train, loss))
  print(train_val)
  print(loss_value)
