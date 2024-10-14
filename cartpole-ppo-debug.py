import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras

class PPOAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.actor = self._build_actor()
        self.critic = self._build_critic()
        self.optimizer = keras.optimizers.Adam(learning_rate=0.0003)

    def _build_actor(self):
        inputs = keras.layers.Input(shape=(self.state_dim,))
        x = keras.layers.Dense(64, activation='relu')(inputs)
        x = keras.layers.Dense(64, activation='relu')(x)
        outputs = keras.layers.Dense(self.action_dim, activation='softmax')(x)
        return keras.Model(inputs, outputs)

    def _build_critic(self):
        inputs = keras.layers.Input(shape=(self.state_dim,))
        x = keras.layers.Dense(64, activation='relu')(inputs)
        x = keras.layers.Dense(64, activation='relu')(x)
        outputs = keras.layers.Dense(1, activation=None)(x)
        return keras.Model(inputs, outputs)

    def get_action(self, state):
        probs = self.actor.predict(np.array([state]), verbose=0)[0]
        action = np.random.choice(self.action_dim, p=probs)
        return action, probs

    @tf.function
    def train_step(self, states, actions, rewards, next_states, dones, old_probs):
        with tf.GradientTape() as tape:
            # Actor loss
            new_probs = self.actor(states, training=True)
            advantages = rewards + 0.99 * self.critic(next_states) * (1 - dones) - self.critic(states)
            advantages = tf.stop_gradient(advantages)
            
            actions_one_hot = tf.one_hot(actions, self.action_dim)
            new_responsible_outputs = tf.reduce_sum(new_probs * actions_one_hot, axis=1)
            old_responsible_outputs = tf.reduce_sum(old_probs * actions_one_hot, axis=1)
            
            ratio = new_responsible_outputs / old_responsible_outputs
            clipped_ratio = tf.clip_by_value(ratio, 0.8, 1.2)
            actor_loss = -tf.reduce_mean(tf.minimum(ratio * advantages, clipped_ratio * advantages))
            
            # Critic loss
            critic_value = self.critic(states, training=True)
            critic_loss = tf.reduce_mean(tf.square(rewards + 0.99 * self.critic(next_states) * (1 - dones) - critic_value))
            
            # Total loss
            loss = actor_loss + 0.5 * critic_loss

        grads = tape.gradient(loss, self.actor.trainable_variables + self.critic.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.actor.trainable_variables + self.critic.trainable_variables))

        return loss

def train(agent, env, episodes=1000, max_steps=500):
    for episode in range(episodes):
        state, _ = env.reset()
        episode_reward = 0
        states, actions, rewards, next_states, dones, old_probs = [], [], [], [], [], []

        for step in range(max_steps):
            action, probs = agent.get_action(state)
            next_state, reward, done, _, _ = env.step(action)

            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            dones.append(float(done))  # Convert boolean to float
            old_probs.append(probs)

            episode_reward += reward
            state = next_state

            if done:
                break

        # Train after each episode
        loss = agent.train_step(
            tf.convert_to_tensor(states, dtype=tf.float32),
            tf.convert_to_tensor(actions, dtype=tf.int32),
            tf.convert_to_tensor(rewards, dtype=tf.float32),
            tf.convert_to_tensor(next_states, dtype=tf.float32),
            tf.convert_to_tensor(dones, dtype=tf.float32),
            tf.convert_to_tensor(old_probs, dtype=tf.float32)
        )

        if episode % 10 == 0:
            print(f"Episode {episode}, Reward: {episode_reward}, Loss: {loss.numpy()}")

if __name__ == "__main__":
    env = gym.make('CartPole-v1')
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    agent = PPOAgent(state_dim, action_dim)
    train(agent, env)