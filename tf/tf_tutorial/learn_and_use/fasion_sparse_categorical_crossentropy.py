# TensorFlow and tf.keras
import tensorflow as tf
print(tf.__version__)
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                             'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
print train_images.shape
print train_labels
#plt.figure()
#plt.imshow(train_images[0])
#plt.colorbar()
#plt.grid(False)
#plt.show()

train_images = train_images / 255.0
test_images = test_images / 255.0

#plt.figure(figsize=(10,10))
#for i in range(25):
#    plt.subplot(5,5,i+1)
#    plt.grid(False)
#    plt.imshow(train_images[i], cmap=plt.cm.binary)
#    #plt.xlabel(class_names[train_labels[i]])
#plt.show()

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])
print model.summary()

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_images,train_labels,epochs=1)

print model.evaluate(test_images, test_labels)
predictions = model.predict(test_images)
print predictions

print np.argmax(predictions[0])
print test_labels[0]

