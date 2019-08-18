#!/usr/bin/python
import tensorflow as tf

tf.enable_eager_execution()

print(tf.add(1, 2))
print(tf.add([1, 2], [3, 4]))
print(tf.square(5))
print(tf.reduce_sum([1, 2, 3]))
print(tf.encode_base64("hello world"))

# Operator overloading is also supported
print(tf.square(2) + tf.square(3))

x = tf.matmul([[1]], [[2, 3]])
print(x.shape)
print(x.dtype)
print x

import numpy as np

ndarray = np.ones([3, 3])
print ndarray

print("TensorFlow operations convert numpy arrays to Tensors automatically")
tensor = tf.multiply(ndarray, 42)
print(tensor)


print("And NumPy operations convert Tensors to numpy arrays automatically")
print(np.add(tensor, 1))

print("The .numpy() method explicitly converts a Tensor to a numpy array")
print(tensor.numpy())

x = tf.random_uniform([3, 3])

print("Is there a GPU available: "),
print(tf.test.is_gpu_available())

print("Is the Tensor on GPU #0:  "),
print(x.device.endswith('GPU:0'))

ds_tensors = tf.data.Dataset.from_tensor_slices([1, 2, 3, 4, 5, 6])
print ds_tensors

# Create a CSV file
import tempfile
_, filename = tempfile.mkstemp()

with open(filename, 'w') as f:
  f.write("""Line 1
Line 2
Line 3
  """)

ds_file = tf.data.TextLineDataset(filename)

def print_ds(xs):
    print('Elements:')
    for x in xs:
      print(x)


#ds_tensors = ds_tensors.map(tf.square).shuffle(2).batch(2)
ds_tensors = ds_tensors.map(tf.square)
print_ds(ds_tensors)
ds_tensors = ds_tensors.shuffle(2)
print_ds(ds_tensors)
ds_tensors = ds_tensors.batch(2)
print_ds(ds_tensors)


ds_file = ds_file.batch(2)
print_ds(ds_file)

