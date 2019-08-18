import tensorflow as tf
 
a=tf.constant([[1,1],[2,2],[3,3]],dtype=tf.float32)
b=tf.constant([1,-1],dtype=tf.float32)
c=tf.constant([1],dtype=tf.float32)
 
with tf.Session() as sess:
    print('bias_add:')
    print(sess.run(tf.nn.bias_add(a, b)))
    print(sess.run(a+ b))
    print(sess.run(a+ c))
