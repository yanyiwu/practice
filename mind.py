import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

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

        # Multi-interest extraction
        self.interest_extractor = layers.LSTM(embedding_dim, return_sequences=True)
        self.interest_evolving = layers.MultiHeadAttention(num_heads=1, key_dim=embedding_dim)

        # Capsule network for interest clustering
        self.capsule_network = layers.Dense(max_interests * embedding_dim)

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

        # Extract multiple interests
        interest_features = self.interest_extractor(history_emb)
        # interest_features: (batch_size, seq_length, embedding_dim)
        # Evolve interests using MultiHeadAttention
        q = tf.expand_dims(user_emb, axis=1)
        # q: (batch_size, 1, embedding_dim)
        k = interest_features
        # k: (batch_size, seq_length, embedding_dim)
        v = interest_features
        # v: (batch_size, seq_length, embedding_dim)
        evolved_interests = self.interest_evolving(
            query=q,
            key=k,
            value=v
        )
        # evolved_interests: (batch_size, 1, embedding_dim)
        evolved_interests = tf.squeeze(evolved_interests, axis=1)
        # evolved_interests: (batch_size, embedding_dim)

        # Cluster interests using capsule network
        capsule_output = self.capsule_network(evolved_interests)
        # capsule_output: (batch_size, max_interests * embedding_dim)
        interest_capsules = tf.reshape(capsule_output, [-1, self.max_interests, self.embedding_dim])
        # interest_capsules: (batch_size, max_interests, embedding_dim)

        # Label-aware attention
        attention_scores = self.label_attention(interest_capsules * item_emb[:, tf.newaxis, :])
        attention_weights = tf.nn.softmax(attention_scores, axis=1)
        
        # Aggregate user interests
        user_representation = tf.reduce_sum(attention_weights * interest_capsules, axis=1)

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
EPOCHS = 5

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
