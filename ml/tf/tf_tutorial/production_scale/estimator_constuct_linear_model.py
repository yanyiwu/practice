#!/usr/bin/env python
# https://www.tensorflow.org/tutorials/estimators/linear
import tensorflow as tf
import tensorflow.feature_column as fc

import os
import sys

import matplotlib.pyplot as plt
#from IPython.display import clear_output

tf.enable_eager_execution()


models_path = os.path.join(os.getcwd(), 'models')

sys.path.append(models_path)

from official.wide_deep import census_dataset
from official.wide_deep import census_main

census_dataset.download("/tmp/census_data/")

#export PYTHONPATH=${PYTHONPATH}:"$(pwd)/models"
#running from python you need to set the `os.environ` or the subprocess will not see the directory.

if "PYTHONPATH" in os.environ:
      os.environ['PYTHONPATH'] += os.pathsep +  models_path
else:
      os.environ['PYTHONPATH'] = models_path

train_file = "/tmp/census_data/adult.data"
test_file = "/tmp/census_data/adult.test"


import pandas

train_df = pandas.read_csv(train_file, header = None, names = census_dataset._CSV_COLUMNS)
test_df = pandas.read_csv(test_file, header = None, names = census_dataset._CSV_COLUMNS)

train_df.head()

def easy_input_function(df, label_key, num_epochs, shuffle, batch_size):
  label = df[label_key]
  ds = tf.data.Dataset.from_tensor_slices((dict(df),label))

  if shuffle:
    ds = ds.shuffle(10000)

  ds = ds.batch(batch_size).repeat(num_epochs)

  return ds

import inspect
print(inspect.getsource(census_dataset.input_fn))


ds = census_dataset.input_fn(train_file, num_epochs=5, shuffle=True, batch_size=10)

for feature_batch, label_batch in ds.take(1):
  print('Feature keys:', list(feature_batch.keys())[:5])
  print()
  print('Age batch   :', feature_batch['age'])
  print()
  print('Label batch :', label_batch )


import functools

train_inpf = functools.partial(census_dataset.input_fn, train_file, num_epochs=2, shuffle=True, batch_size=64)
test_inpf = functools.partial(census_dataset.input_fn, test_file, num_epochs=1, shuffle=False, batch_size=64)


age = fc.numeric_column('age')

print(fc.input_layer(feature_batch, [age]).numpy())

classifier = tf.estimator.LinearClassifier(feature_columns=[age])
classifier.train(train_inpf)
result = classifier.evaluate(test_inpf)

#clear_output()  # used for display in notebook
print(result)
education_num = tf.feature_column.numeric_column('education_num')
capital_gain = tf.feature_column.numeric_column('capital_gain')
capital_loss = tf.feature_column.numeric_column('capital_loss')
hours_per_week = tf.feature_column.numeric_column('hours_per_week')
my_numeric_columns = [age,education_num, capital_gain, capital_loss, hours_per_week]

t = fc.input_layer(feature_batch, my_numeric_columns).numpy()
print(t)


classifier = tf.estimator.LinearClassifier(feature_columns=my_numeric_columns)
classifier.train(train_inpf)

result = classifier.evaluate(test_inpf)

#clear_output()

for key,value in sorted(result.items()):
  print('%s: %s' % (key, value))

relationship = fc.categorical_column_with_vocabulary_list(
    'relationship',
    ['Husband', 'Not-in-family', 'Wife', 'Own-child', 'Unmarried', 'Other-relative'])


fc.input_layer(feature_batch, [age, fc.indicator_column(relationship)])

occupation = tf.feature_column.categorical_column_with_hash_bucket(
    'occupation', hash_bucket_size=1000)

for item in feature_batch['occupation'].numpy():
  print(item.decode())


occupation_result = fc.input_layer(feature_batch, [fc.indicator_column(occupation)])
occupation_result.numpy().shape

tf.argmax(occupation_result, axis=1).numpy()

education = tf.feature_column.categorical_column_with_vocabulary_list(
    'education', [
            'Bachelors', 'HS-grad', '11th', 'Masters', '9th', 'Some-college',
            'Assoc-acdm', 'Assoc-voc', '7th-8th', 'Doctorate', 'Prof-school',
            '5th-6th', '10th', '1st-4th', 'Preschool', '12th'])

marital_status = tf.feature_column.categorical_column_with_vocabulary_list(
    'marital_status', [
            'Married-civ-spouse', 'Divorced', 'Married-spouse-absent',
            'Never-married', 'Separated', 'Married-AF-spouse', 'Widowed'])

workclass = tf.feature_column.categorical_column_with_vocabulary_list(
    'workclass', [
            'Self-emp-not-inc', 'Private', 'State-gov', 'Federal-gov',
            'Local-gov', '?', 'Self-emp-inc', 'Without-pay', 'Never-worked'])

my_categorical_columns = [relationship, occupation, education, marital_status, workclass]


classifier = tf.estimator.LinearClassifier(feature_columns=my_numeric_columns+my_categorical_columns)
classifier.train(train_inpf)
result = classifier.evaluate(test_inpf)

#clear_output()

for key,value in sorted(result.items()):
  print('%s: %s' % (key, value))


age_buckets = tf.feature_column.bucketized_column(
    age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])

fc.input_layer(feature_batch, [age, age_buckets]).numpy()

education_x_occupation = tf.feature_column.crossed_column(
    ['education', 'occupation'], hash_bucket_size=1000)

age_buckets_x_education_x_occupation = tf.feature_column.crossed_column(
    [age_buckets, 'education', 'occupation'], hash_bucket_size=1000)

import tempfile

base_columns = [
    education, marital_status, relationship, workclass, occupation,
    age_buckets,
]

crossed_columns = [
    tf.feature_column.crossed_column(
            ['education', 'occupation'], hash_bucket_size=1000),
    tf.feature_column.crossed_column(
            [age_buckets, 'education', 'occupation'], hash_bucket_size=1000),
]

model = tf.estimator.LinearClassifier(
    model_dir=tempfile.mkdtemp(),
    feature_columns=base_columns + crossed_columns,
    optimizer=tf.train.FtrlOptimizer(learning_rate=0.1))

train_inpf = functools.partial(census_dataset.input_fn, train_file,
                                                             num_epochs=40, shuffle=True, batch_size=64)

model.train(train_inpf)

results = model.evaluate(test_inpf)

#clear_output()

for key,value in sorted(result.items()):
  print('%s: %0.2f' % (key, value))

import numpy as np

#predict_df = test_df[:20].copy()
#
#pred_iter = model.predict(
#    lambda:easy_input_function(predict_df, label_key='income_bracket',
#                                                             num_epochs=1, shuffle=False, batch_size=10))
#
#classes = np.array(['<=50K', '>50K'])
#pred_class_id = []
#
#for pred_dict in pred_iter:
#  pred_class_id.append(pred_dict['class_ids'])
#
#  t = np.array(pred_class_id)
#  predict_df['predicted_class'] = classes[t]
#  predict_df['correct'] = predict_df['predicted_class'] == predict_df['income_bracket']
#
#  #clear_output()
#
#  predict_df[['income_bracket','predicted_class', 'correct']]


model_l1 = tf.estimator.LinearClassifier(
    feature_columns=base_columns + crossed_columns,
    optimizer=tf.train.FtrlOptimizer(
            learning_rate=0.1,
            l1_regularization_strength=10.0,
            l2_regularization_strength=0.0))

model_l1.train(train_inpf)

results = model_l1.evaluate(test_inpf)
#clear_output()
for key in sorted(results):
  print('%s: %0.2f' % (key, results[key]))


model_l2 = tf.estimator.LinearClassifier(
    feature_columns=base_columns + crossed_columns,
    optimizer=tf.train.FtrlOptimizer(
        learning_rate=0.1,
        l1_regularization_strength=0.0,
        l2_regularization_strength=10.0))

model_l2.train(train_inpf)

results = model_l2.evaluate(test_inpf)
#clear_output()
for key in sorted(results):
  print('%s: %0.2f' % (key, results[key]))

def get_flat_weights(model):
  weight_names = [
      name for name in model.get_variable_names()
      if "linear_model" in name and "Ftrl" not in name]

  weight_values = [model.get_variable_value(name) for name in weight_names]

  weights_flat = np.concatenate([item.flatten() for item in weight_values], axis=0)

  return weights_flat

weights_flat = get_flat_weights(model)
weights_flat_l1 = get_flat_weights(model_l1)
weights_flat_l2 = get_flat_weights(model_l2)

weight_mask = weights_flat != 0

weights_base = weights_flat[weight_mask]
weights_l1 = weights_flat_l1[weight_mask]
weights_l2 = weights_flat_l2[weight_mask]

plt.figure()
_ = plt.hist(weights_base, bins=np.linspace(-3,3,30))
plt.title('Base Model')
plt.ylim([0,500])

plt.figure()
_ = plt.hist(weights_l1, bins=np.linspace(-3,3,30))
plt.title('L1 - Regularization')
plt.ylim([0,500])

plt.figure()
_ = plt.hist(weights_l2, bins=np.linspace(-3,3,30))
plt.title('L2 - Regularization')
_=plt.ylim([0,500])

