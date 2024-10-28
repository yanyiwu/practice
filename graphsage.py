import tensorflow as tf
from tensorflow import keras
import numpy as np

class SAGEConv(keras.layers.Layer):
    def __init__(self, in_channels, out_channels, aggregator_type='mean'):
        super(SAGEConv, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.aggregator_type = aggregator_type
        self.weight = None
        self.bias = None

    def build(self, input_shape):
        self.weight = self.add_weight(
            shape=(self.in_channels, self.out_channels),
            initializer='glorot_uniform',
            name='weight'
        )
        self.bias = self.add_weight(
            shape=(self.out_channels,),
            initializer='zeros',
            name='bias'
        )

    def aggregate(self, neighbor_features, adj_matrix):
        # neighbor_features shape: (1, num_nodes, num_features)
        # adj_matrix shape: (1, num_nodes, num_nodes)   
        if self.aggregator_type == 'mean':
            # Use the adjacency matrix for weighted aggregation
            neighbor_sum = tf.matmul(adj_matrix, neighbor_features)
            # neighbor_sum shape: (1, num_nodes, num_features)
            neighbor_count = tf.reduce_sum(adj_matrix, axis=-1, keepdims=True)
            # neighbor_count shape: (1, num_nodes, 1)
            return neighbor_sum / (neighbor_count + 1e-6)  # Add epsilon to avoid division by zero
        elif self.aggregator_type == 'max':
            return tf.reduce_max(neighbor_features, axis=1)
        else:
            raise ValueError(f"Unsupported aggregator type: {self.aggregator_type}")

    def call(self, inputs, adj_matrix):
        self_features, neighbor_features = inputs
        # self_features shape: (1, num_nodes, num_features) 
        # neighbor_features shape: (1, num_nodes, num_features)
        aggregated = self.aggregate(neighbor_features, adj_matrix)
        # aggregated shape: (1, num_nodes, num_features)
        combined = self_features + aggregated
        # combined shape: (1, num_nodes, num_features)
        output = tf.matmul(combined, self.weight) + self.bias
        # output shape: (1, num_nodes, num_features)
        return tf.nn.relu(output)

class GraphSAGE(keras.Model):
    def __init__(self, layer_sizes, aggregator_type='mean'):
        super(GraphSAGE, self).__init__()
        self.sage_layers = []
        for i in range(len(layer_sizes) - 1):
            self.sage_layers.append(SAGEConv(layer_sizes[i], layer_sizes[i+1], aggregator_type))

    def call(self, inputs):
        x, adj_matrix = inputs
        # x shape: (1, num_nodes, num_features)
        # adj_matrix shape: (1, num_nodes, num_nodes)
        for layer in self.sage_layers:
            neighbor_features = x
            # neighbor_features shape: (1, num_nodes, num_features) 
            x = layer((x, neighbor_features), adj_matrix)
            # x shape: (1, num_nodes, num_features)
        return x

# Demo
def graphsage_demo():
    num_nodes = 1000
    num_features = 16
    hidden_sizes = [16, 32, 64]
    num_classes = 10

    # Generate dummy data
    node_features = np.random.randn(num_nodes, num_features).astype(np.float32)
    adj_matrix = np.random.randint(0, 2, (num_nodes, num_nodes)).astype(np.float32)
    labels = np.random.randint(0, num_classes, num_nodes)

    # Create model
    model = GraphSAGE([num_features] + hidden_sizes + [num_classes])

    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.01),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )

    # Prepare inputs
    inputs = (
        tf.expand_dims(node_features, 0),  # Add batch dimension
        tf.expand_dims(adj_matrix, 0)  # Add batch dimension
    )
    # inputs shape: [(1, num_nodes, num_features), (1, num_nodes, num_nodes)]
    labels_tensor = tf.expand_dims(labels, 0)  # Add batch dimension
    # labels_tensor shape: (1, num_nodes)
    # Train model
    for epoch in range(10):
        loss, accuracy = model.train_on_batch(inputs, labels_tensor)
        print(f"Epoch {epoch + 1}/10 - Loss: {loss:.4f} - Accuracy: {accuracy:.4f}")

    # Evaluate model
    test_loss, test_accuracy = model.evaluate(inputs, labels_tensor)
    print(f"Test accuracy: {test_accuracy:.4f}")

if __name__ == "__main__":
    graphsage_demo()
