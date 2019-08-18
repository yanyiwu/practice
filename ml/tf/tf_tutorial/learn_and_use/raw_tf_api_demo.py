import sys
import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf

def print_tensor(te):
    init_op = tf.global_variables_initializer()
    #run the graph
    with tf.Session() as sess:
        sess.run(init_op) #execute init_op
        print (sess.run(te))

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder("float", [None, 784])

W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

print_tensor(b)

t = tf.matmul(x, W)
y = tf.nn.softmax(t + b)

y_ = tf.placeholder("float", [None,10])

cross_entropy = -tf.reduce_sum(y_*tf.log(y))

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)


#init = tf.initialize_all_variables()
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))


print sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})

