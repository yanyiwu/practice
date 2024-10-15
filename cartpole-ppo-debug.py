import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras

class PPOAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        # PPO使用单独的actor和critic网络,而不是DQN中的单一Q网络
        self.actor = self._build_actor()
        self.critic = self._build_critic()
        self.optimizer = keras.optimizers.Adam(learning_rate=0.0003)

    def _build_actor(self):
        # Actor网络输出动作概率分布,而不是DQN中的Q值
        inputs = keras.layers.Input(shape=(self.state_dim,))
        x = keras.layers.Dense(64, activation='relu')(inputs)
        x = keras.layers.Dense(64, activation='relu')(x)
        outputs = keras.layers.Dense(self.action_dim, activation='softmax')(x)
        #  intputs shape: (batch_size, state_dim)
        #  outputs shape: (batch_size, action_dim)
        return keras.Model(inputs, outputs)

    def _build_critic(self):
        # Critic网络估计状态值,而不是DQN中的动作值
        inputs = keras.layers.Input(shape=(self.state_dim,))
        x = keras.layers.Dense(64, activation='relu')(inputs)
        x = keras.layers.Dense(64, activation='relu')(x)
        outputs = keras.layers.Dense(1, activation=None)(x)
        #  intputs shape: (batch_size, state_dim)
        #  outputs shape: (batch_size, 1)   
        return keras.Model(inputs, outputs)

    def get_action(self, state):
        # PPO基于概率选择动作,而不是DQN中的ε-greedy策略
        probs = self.actor.predict(np.array([state]), verbose=0)[0]
        # probs shape: (action_dim,)
        action = np.random.choice(self.action_dim, p=probs)
        return action, probs

    @tf.function
    def train_step(self, states, actions, rewards, next_states, dones, old_probs):
        with tf.GradientTape() as tape:
            # PPO使用优势函数和重要性采样比率,这在DQN中不存在
            # states shape: (batch_size, state_dim)
            # actions shape: (batch_size,)
            # rewards shape: (batch_size,)
            # next_states shape: (batch_size, state_dim)
            # dones shape: (batch_size,)
            # old_probs shape: (batch_size, action_dim) 
            new_probs = self.actor(states, training=True)
            # new_probs shape: (batch_size, action_dim)
            advantages = rewards + 0.99 * self.critic(next_states) * (1 - dones) - self.critic(states)
            advantages = tf.stop_gradient(advantages)
            
            actions_one_hot = tf.one_hot(actions, self.action_dim)
            new_responsible_outputs = tf.reduce_sum(new_probs * actions_one_hot, axis=1)
            old_responsible_outputs = tf.reduce_sum(old_probs * actions_one_hot, axis=1)
            
            # PPO的核心:计算策略比率并裁剪
            ratio = new_responsible_outputs / old_responsible_outputs
            clipped_ratio = tf.clip_by_value(ratio, 0.8, 1.2)
            actor_loss = -tf.reduce_mean(tf.minimum(ratio * advantages, clipped_ratio * advantages))
            
            # Critic损失类似于DQN,都基于TD误差,但估计的是状态值而非Q值
            critic_value = self.critic(states, training=True)
            critic_loss = tf.reduce_mean(tf.square(rewards + 0.99 * self.critic(next_states) * (1 - dones) - critic_value))
            
            # 总损失包括actor和critic损失
            loss = actor_loss + 0.5 * critic_loss

        # 同时更新actor和critic网络
        grads = tape.gradient(loss, self.actor.trainable_variables + self.critic.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.actor.trainable_variables + self.critic.trainable_variables))

        return loss

def train(agent, env, episodes=100, max_steps=200):
    for episode in range(episodes):
        state, _ = env.reset()
        episode_reward = 0
        # PPO收集完整轨迹,而不是DQN中的单步经验
        states, actions, rewards, next_states, dones, old_probs = [], [], [], [], [], []

        for step in range(max_steps):
            action, probs = agent.get_action(state)
            next_state, reward, done, _, _ = env.step(action)

            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            dones.append(float(done))
            old_probs.append(probs)

            episode_reward += reward
            state = next_state

            if done:
                break

        # PPO在每个episode结束后进行批量更新,而不是DQN的频繁更新
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

def test_agent(agent, env, episodes=10):
    total_rewards = []
    for episode in range(episodes):
        state, _ = env.reset()
        episode_reward = 0
        done = False
        while not done:
            action, _ = agent.get_action(state)
            next_state, reward, done, _, _ = env.step(action)
            episode_reward += reward
            state = next_state
        total_rewards.append(episode_reward)
    
    avg_reward = np.mean(total_rewards)
    print(f"Average reward over {episodes} episodes: {avg_reward}")
    return avg_reward

if __name__ == "__main__":
    env = gym.make('CartPole-v1')
    state_dim = env.observation_space.shape[0]
    # state_dim = 4 (position, velocity, angle, angular velocity)
    action_dim = env.action_space.n
    # action_dim = 2 (left, right)  

    agent = PPOAgent(state_dim, action_dim)
    train(agent, env)

    # 测试训练好的agent
    test_agent(agent, env)
