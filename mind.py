import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class SimpleCapsule(layers.Layer):
    def __init__(self, num_capsules, dim_capsules):
        super(SimpleCapsule, self).__init__()
        self.num_capsules = num_capsules
        self.dim_capsules = dim_capsules
        self.W = self.add_weight(shape=(num_capsules, dim_capsules, dim_capsules),
                                 initializer='glorot_uniform',
                                 name='W')

    def call(self, inputs):
        # inputs shape: (batch_size, dim_capsules)
        u = tf.expand_dims(inputs, axis=1)  # (batch_size, 1, dim_capsules)
        u = tf.tile(u, [1, self.num_capsules, 1])  # (batch_size, num_capsules, dim_capsules)
        
        # Simple routing: just apply the transformation
        s = tf.einsum('bni,nij->bnj', u, self.W)
        # s: (batch_size, num_capsules, dim_capsules)   
        
        # Apply squash activation
        squared_norm = tf.reduce_sum(tf.square(s), axis=-1, keepdims=True)
        # squared_norm: (batch_size, num_capsules, 1)   
        scale = squared_norm / (1 + squared_norm) / tf.sqrt(squared_norm + 1e-8)
        # scale: (batch_size, num_capsules, 1)
        v = scale * s
        # v: (batch_size, num_capsules, dim_capsules)
        return v

class MINDModel(keras.Model):
    def __init__(self, num_users, num_items, embedding_dim, max_interests, num_sampled_interests):
        super(MINDModel, self).__init__()
        self.num_users = num_users
        self.num_items = num_items
        self.embedding_dim = embedding_dim
        self.max_interests = max_interests
        self.num_sampled_interests = num_sampled_interests

        # User and item embeddings
        self.user_embedding = layers.Embedding(num_users, embedding_dim)
        self.item_embedding = layers.Embedding(num_items, embedding_dim)

        # 将 LSTM 替换为 MultiHeadAttention 用于兴趣提取
        self.interest_extractor = layers.MultiHeadAttention(
            num_heads=4
        )
        
        # 保持原有的 MultiHeadAttention 用于兴趣演化
        self.interest_evolving = layers.MultiHeadAttention(num_heads=1)

        # 位置编码层
        self.positional_encoding = layers.Embedding(input_dim=1000, output_dim=embedding_dim)  # 假设最大序列长度为1000

        # Capsule network for interest clustering
        self.capsule_network = SimpleCapsule(max_interests, embedding_dim)
        # capsule_network: (batch_size, embedding_dim) -> (batch_size, max_interests, embedding_dim)
        # Label-aware attention
        self.label_attention = layers.Dense(1)

    def call(self, inputs):
        user_ids, item_ids, user_history = inputs
        
        # Embed users and items
        user_emb = self.user_embedding(user_ids)
        # user_emb: (batch_size, embedding_dim)
        item_emb = self.item_embedding(item_ids)
        # item_emb: (batch_size, embedding_dim)
        history_emb = self.item_embedding(user_history)
        # history_emb: (batch_size, seq_length, embedding_dim)

        # Add position encoding
        positions = tf.range(start=0, limit=tf.shape(user_history)[1], delta=1)
        # positions: (seq_length,)  
        positional_encodings = self.positional_encoding(positions)
        # positional_encodings: (seq_length, embedding_dim)
        history_emb = history_emb + positional_encodings
        # history_emb: (batch_size, seq_length, embedding_dim)

        # Extract multiple interests
        # 1. Use MultiHeadAttention to extract interest features from user history
        interest_features = self.interest_extractor(
            query=history_emb,
            key=history_emb,
            value=history_emb
        )
        # interest_features: (batch_size, seq_length, embedding_dim)
        
        # Evolve interests using MultiHeadAttention
        q = tf.expand_dims(user_emb, axis=1)
        # q: (batch_size, 1, embedding_dim)
        evolved_interests = self.interest_evolving(query=q, key=interest_features, value=interest_features)
        evolved_interests = tf.squeeze(evolved_interests, axis=1)
        # evolved_interests: (batch_size, embedding_dim)

        # Cluster interests using capsule network
        # 3. Use capsule network to cluster interests
        capsule_output = self.capsule_network(evolved_interests)
        # capsule_output shape: (batch_size, max_interests, embedding_dim)

        # Label-aware attention
        attention_scores = self.label_attention(capsule_output * item_emb[:, tf.newaxis, :])
        attention_weights = tf.nn.softmax(attention_scores, axis=1)
        
        # Aggregate user interests
        user_representation = tf.reduce_sum(attention_weights * capsule_output, axis=1)

        # Compute final score
        scores = tf.reduce_sum(user_representation * item_emb, axis=-1)
        return scores

# Hyperparameters
NUM_USERS = 10000
NUM_ITEMS = 50000
EMBEDDING_DIM = 64
MAX_INTERESTS = 5
NUM_SAMPLED_INTERESTS = 3
BATCH_SIZE = 256
EPOCHS = 1

# Create and compile the model
model = MINDModel(NUM_USERS, NUM_ITEMS, EMBEDDING_DIM, MAX_INTERESTS, NUM_SAMPLED_INTERESTS)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Generate some dummy data for demonstration
num_samples = 100000
max_history_length = 20

user_ids = np.random.randint(0, NUM_USERS, num_samples)
item_ids = np.random.randint(0, NUM_ITEMS, num_samples)
user_history = np.random.randint(0, NUM_ITEMS, (num_samples, max_history_length))
labels = np.random.randint(0, 2, num_samples)  # Binary labels: 0 or 1

# Train the model
model.fit([user_ids, item_ids, user_history], labels, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.2)

# Function to get top-k recommendations for a user
def get_top_k_recommendations(model, user_id, user_history, k=10):
    user_ids = np.full(NUM_ITEMS, user_id)
    item_ids = np.arange(NUM_ITEMS)
    user_history = np.tile(user_history, (NUM_ITEMS, 1))
    
    scores = model.predict([user_ids, item_ids, user_history])
    top_k_items = item_ids[np.argsort(scores)[-k:]]
    
    return top_k_items[::-1]  # Reverse to get descending order

# Example usage
user_id = 42
user_history = np.random.randint(0, NUM_ITEMS, max_history_length)
top_recommendations = get_top_k_recommendations(model, user_id, user_history, k=10)
print(f"Top 10 recommendations for user {user_id}:", top_recommendations)
