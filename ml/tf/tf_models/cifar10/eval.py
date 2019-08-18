#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import math
import time

import numpy as np
import tensorflow as tf

import model
import cifar10_input

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('eval_dir', './output/eval',
                           """Directory where to write event logs.""")
tf.app.flags.DEFINE_string('checkpoint_dir', './output/train',
                           """Directory where to read model checkpoints.""")
tf.app.flags.DEFINE_integer('num_examples', 10000,
                            """Number of examples to run.""")

def evaluate():
  with tf.Graph().as_default() as g:
    # Get images and labels for CIFAR-10.
    images, labels = cifar10_input.inputs(eval_data=True)

    logits = model.inference(images)

    top_k_op = tf.nn.in_top_k(logits, labels, 1)

    saver = tf.train.Saver()

    # Build the summary operation based on the TF collection of Summaries.
    summary_op = tf.summary.merge_all()
    summary_writer = tf.summary.FileWriter(FLAGS.eval_dir, g)
    with tf.Session() as sess:
      ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
      if ckpt and ckpt.model_checkpoint_path:
        # Restores from checkpoint
        saver.restore(sess, ckpt.model_checkpoint_path)
        # Assuming model_checkpoint_path looks something like:
        #   /my-favorite-path/cifar10_train/model.ckpt-0,
        # extract global_step from it.
        global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
      else:
        print('No checkpoint file found')
        return

      # Start the queue runners.
      coord = tf.train.Coordinator()
      try:
        threads = []
        for qr in tf.get_collection(tf.GraphKeys.QUEUE_RUNNERS):
          threads.extend(qr.create_threads(sess, coord=coord, daemon=True,
                                           start=True))

        num_iter = int(math.ceil(FLAGS.num_examples / FLAGS.batch_size))
        true_count = 0  # Counts the number of correct predictions.
        total_sample_count = num_iter * FLAGS.batch_size
        step = 0
        while step < num_iter and not coord.should_stop():
          predictions = sess.run([top_k_op])
          true_count += np.sum(predictions)
          step += 1

        # Compute precision @ 1.
        precision = true_count / total_sample_count
        print('%s: precision @ 1 = %.3f' % (datetime.now(), precision))

        summary = tf.Summary()
        summary.ParseFromString(sess.run(summary_op))
        summary.value.add(tag='Precision @ 1', simple_value=precision)
        summary_writer.add_summary(summary, global_step)
      except Exception as e:  # pylint: disable=broad-except
        coord.request_stop(e)

      coord.request_stop()
      coord.join(threads, stop_grace_period_secs=10)

def main(argv=None):  # pylint: disable=unused-argument
  evaluate()

if __name__ == '__main__':
  tf.app.run()
