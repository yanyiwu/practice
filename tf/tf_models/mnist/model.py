#!/usr/bin/env python
# from tensorflow/models/official/mnist/mnist.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app as absl_app
from absl import flags
import tensorflow as tf  # pylint: disable=g-bad-import-order

# remove official deps
import dataset

flags.DEFINE_string(name='data_dir', default='./mnist_data', help='')
flags.DEFINE_string(name='model_dir', default='./mnist_model', help='')
flags.DEFINE_integer(name='batch_size', default=100, help='')
flags.DEFINE_integer(name='train_epochs', default=1, help='')
flags.DEFINE_string(name='data_format', default='channels_last', help='')

LEARNING_RATE = 1e-4


def create_model():
  input_shape = [28, 28, 1]
  l = tf.keras.layers
  max_pool = l.MaxPooling2D(
      (2, 2), (2, 2), padding='same', data_format=flags.FLAGS.data_format)
  # The model consists of a sequential chain of layers, so tf.keras.Sequential
  # (a subclass of tf.keras.Model) makes for a compact description.
  m = tf.keras.Sequential(
      [
          l.Reshape(
              target_shape=input_shape,
              input_shape=(28 * 28,)),
          l.Conv2D(
              32,
              5,
              padding='same',
              data_format=flags.FLAGS.data_format,
              activation=tf.nn.relu),
          max_pool,
          l.Conv2D(
              64,
              5,
              padding='same',
              data_format=flags.FLAGS.data_format,
              activation=tf.nn.relu),
          max_pool,
          l.Flatten(),
          l.Dense(1024, activation=tf.nn.relu),
          l.Dropout(0.4),
          l.Dense(10)
      ])
  return m


def model_fn(features, labels, mode, params):
  """The model_fn argument for creating an Estimator."""
  model = create_model()
  image = features
  print(features)
  print(labels)

  if mode == tf.estimator.ModeKeys.PREDICT:
    logits = model(image, training=False)
    predictions = {
        'classes': tf.argmax(logits, axis=1),
        'probabilities': tf.nn.softmax(logits),
    }
    return tf.estimator.EstimatorSpec(
        mode=tf.estimator.ModeKeys.PREDICT,
        predictions=predictions,
        export_outputs={
            'classify': tf.estimator.export.PredictOutput(predictions)
        })
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE)

    logits = model(image, training=True)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
    accuracy = tf.metrics.accuracy(
        labels=labels, predictions=tf.argmax(logits, axis=1))

    # Name tensors to be logged with LoggingTensorHook.
    tf.identity(LEARNING_RATE, 'learning_rate')
    tf.identity(loss, 'cross_entropy')
    tf.identity(accuracy[1], name='train_accuracy')

    # Save accuracy scalar to Tensorboard output.
    tf.summary.scalar('train_accuracy', accuracy[1])

    return tf.estimator.EstimatorSpec(
        mode=tf.estimator.ModeKeys.TRAIN,
        loss=loss,
        train_op=optimizer.minimize(loss, tf.train.get_or_create_global_step()))
  if mode == tf.estimator.ModeKeys.EVAL:
    logits = model(image, training=False)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
    return tf.estimator.EstimatorSpec(
        mode=tf.estimator.ModeKeys.EVAL,
        loss=loss,
        eval_metric_ops={
            'accuracy':
                tf.metrics.accuracy(
                    labels=labels, predictions=tf.argmax(logits, axis=1)),
        })


def run_mnist():
  data_format = 'channels_last'
  mnist_classifier = tf.estimator.Estimator(
      model_fn=model_fn,
      model_dir=flags.FLAGS.model_dir,
      params={
          'data_format': data_format,
      })

  # Set up training and evaluation input functions.
  def train_input_fn():
    return dataset.dataset(flags.FLAGS.data_dir, 'train-images-idx3-ubyte', 'train-labels-idx1-ubyte').cache().shuffle(buffer_size=50000).batch(flags.FLAGS.batch_size)

  def eval_input_fn():
    return dataset.dataset(flags.FLAGS.data_dir, 't10k-images-idx3-ubyte', 't10k-labels-idx1-ubyte').batch(flags.FLAGS.batch_size).make_one_shot_iterator().get_next()

  # Set up hook that outputs training logs every 100 steps.
  tensors_to_log = dict((x, x) for x in ['learning_rate',
                                        'cross_entropy',
                                        'train_accuracy'])
  train_hooks = [
      tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=100)
  ]

  # Train and evaluate model.
  for _ in range(flags.FLAGS.train_epochs):
    mnist_classifier.train(input_fn=train_input_fn, hooks=train_hooks)
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print('\nEvaluation results:\n\t%s\n' % eval_results)

def main(_):
  run_mnist()


if __name__ == '__main__':
  tf.logging.set_verbosity(tf.logging.INFO)
  #define_mnist_flags()
  absl_app.run(main)
