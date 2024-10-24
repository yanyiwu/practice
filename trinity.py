


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class TrinityModel(keras.Model):
    def __init__(self, num_interests, embedding_dim, num_users, num_items):
        super(TrinityModel, self).__init__()
        self.num_interests = num_interests
        self.embedding_dim = embedding_dim
        
        self.user_embedding = layers.Embedding(input_dim=num_users, output_dim=embedding_dim)
        self.item_embedding = layers.Embedding(input_dim=num_items, output_dim=embedding_dim)
        self.interest_vectors = self.add_weight(shape=(num_interests, embedding_dim),
                                                initializer='random_normal',
                                                trainable=True, name='interest_vectors')
        
        self.attention = layers.Dense(num_interests, activation='softmax')
        
    def call(self, inputs):
        user_ids, item_ids = inputs
        user_emb = self.user_embedding(user_ids)
        item_emb = self.item_embedding(item_ids)
        
        # Calculate attention scores for multiple interests
        attention_scores = self.attention(user_emb)
        
        # Weighted sum of interest vectors
        user_interests = tf.matmul(attention_scores, self.interest_vectors)
        
        # Compute similarity between user interests and item
        similarities = tf.reduce_sum(user_interests * item_emb[:, tf.newaxis, :], axis=-1)
        
        # Take the maximum similarity across all interests
        max_similarity = tf.reduce_max(similarities, axis=-1)
        
        return max_similarity

# Hyperparameters
NUM_INTERESTS = 5
EMBEDDING_DIM = 64
BATCH_SIZE = 256
EPOCHS = 5
NUM_USERS = 10000
NUM_ITEMS = 50000

# Create and compile the model
model = TrinityModel(NUM_INTERESTS, EMBEDDING_DIM, NUM_USERS, NUM_ITEMS)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Generate some dummy data for demonstration
num_samples = 100000

user_ids = np.random.randint(0, NUM_USERS, num_samples)
item_ids = np.random.randint(0, NUM_ITEMS, num_samples)
labels = np.random.randint(0, 2, num_samples)  # Binary labels: 0 or 1

# Train the model
model.fit([user_ids, item_ids], labels, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.2)

# Example of using the model for recommendations
test_user_ids = np.array([1, 2, 3])
test_item_ids = np.array([100, 200, 300])
predictions = model.predict([test_user_ids, test_item_ids])
print("Predictions:", predictions)

# Function to get top-k recommendations for a user
def get_top_k_recommendations(model, user_id, k=10):
    user_ids = np.full(NUM_ITEMS, user_id)
    item_ids = np.arange(NUM_ITEMS)
    
    scores = model.predict([user_ids, item_ids])
    top_k_items = item_ids[np.argsort(scores)[-k:]]
    
    return top_k_items[::-1]  # Reverse to get descending order

# Example usage
user_id = 42
top_recommendations = get_top_k_recommendations(model, user_id, k=10)
print(f"Top 10 recommendations for user {user_id}:", top_recommendations)

