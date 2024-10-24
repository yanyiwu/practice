import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Define the LoRA layer
class LoRALayer(layers.Layer):
    def __init__(self, in_features, out_features, rank=4, alpha=1):
        super(LoRALayer, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.alpha = alpha
        
        self.A = self.add_weight(shape=(in_features, rank),
                                 initializer='random_normal',
                                 trainable=True, name='lora_A')
        self.B = self.add_weight(shape=(rank, out_features),
                                 initializer='zeros',
                                 trainable=True, name='lora_B')
        self.scaling = self.alpha / self.rank

    def call(self, inputs):
        return tf.matmul(inputs, self.A) @ self.B * self.scaling

# Define a simple model with LoRA
class SimpleModelWithLoRA(keras.Model):
    def __init__(self, input_dim, hidden_dim, output_dim, lora_rank=4):
        super(SimpleModelWithLoRA, self).__init__()
        self.dense1 = layers.Dense(hidden_dim)
        self.lora = LoRALayer(hidden_dim, hidden_dim, rank=lora_rank)
        self.dense2 = layers.Dense(output_dim)

    def call(self, inputs):
        x = self.dense1(inputs)
        x = x + self.lora(x)  # LoRA as residual
        return self.dense2(x)

# Create and compile the model
input_dim = 784  # for MNIST
hidden_dim = 256
output_dim = 10
model = SimpleModelWithLoRA(input_dim, hidden_dim, output_dim)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Load and preprocess MNIST data
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train.reshape(60000, 784).astype('float32') / 255
x_test = x_test.reshape(10000, 784).astype('float32') / 255

# Train the model
model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.2)

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f'\nTest accuracy: {test_acc}')
