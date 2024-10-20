import tensorflow as tf
import numpy as np

class MoCo(tf.keras.Model):
    def __init__(self, encoder, dim=2048, K=65536, m=0.999, T=0.07):
        super(MoCo, self).__init__()
        self.encoder_q = encoder
        self.encoder_k = tf.keras.models.clone_model(encoder)
        self.dim = dim
        self.K = K
        self.m = m
        self.T = T
        
        self.queue = tf.Variable(tf.math.l2_normalize(tf.random.normal(shape=(dim, K)), axis=0))
        self.queue_ptr = tf.Variable(0)
        
        # Initialize the key encoder with the query encoder weights
        self.encoder_k.set_weights(self.encoder_q.get_weights())
    
    def call(self, inputs):
        # Unpack the inputs tuple
        im_q, im_k = inputs
        
        # Compute query features
        q = self.encoder_q(im_q)  # queries: NxC
        q = tf.math.l2_normalize(q, axis=1)
        
        # Compute key features
        k = tf.stop_gradient(self.encoder_k(im_k))  # keys: NxC
        k = tf.math.l2_normalize(k, axis=1)
        
        # Update key encoder
        for var_q, var_k in zip(self.encoder_q.trainable_variables, self.encoder_k.trainable_variables):
            var_k.assign(self.m * var_k + (1 - self.m) * var_q)
        
        # Compute logits
        l_pos = tf.reduce_sum(q * k, axis=1, keepdims=True)  # Nx1
        l_neg = tf.matmul(q, self.queue)  # NxK
        
        logits = tf.concat([l_pos, l_neg], axis=1)  # Nx(1+K)
        logits /= self.T
        
        # Labels: positives are the 0-th
        labels = tf.zeros(logits.shape[0], dtype=tf.int64)
        
        # Dequeue and enqueue
        self._dequeue_and_enqueue(k)
        
        return logits, labels
    
    @tf.function
    def _dequeue_and_enqueue(self, keys):
        batch_size = keys.shape[0]
        ptr = self.queue_ptr
        
        # Replace the keys at ptr (dequeue and enqueue)
        self.queue[:, ptr:ptr+batch_size].assign(tf.transpose(keys))
        
        # Move pointer
        ptr = (ptr + batch_size) % self.K
        self.queue_ptr.assign(ptr)

# Example usage
encoder = tf.keras.applications.ResNet50(include_top=False, weights=None, pooling='avg')
moco = MoCo(encoder, dim=2048)  # Set dim to match the output of ResNet50

# Create some dummy data
batch_size = 32
im_q = tf.random.normal((batch_size, 224, 224, 3))
im_k = tf.random.normal((batch_size, 224, 224, 3))

# Define the loss function
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# Define the optimizer
optimizer = tf.keras.optimizers.Adam()

# Training step
@tf.function
def train_step(im_q, im_k):
    with tf.GradientTape() as tape:
        logits, labels = moco((im_q, im_k))
        loss = loss_fn(labels, logits)

    gradients = tape.gradient(loss, moco.trainable_variables)
    optimizer.apply_gradients(zip(gradients, moco.trainable_variables))
    return loss

# Perform a single training step
loss = train_step(im_q, im_k)
print(f"Loss: {loss.numpy()}")
