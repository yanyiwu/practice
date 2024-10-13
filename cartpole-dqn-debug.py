import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras
from collections import deque
import random

# 定义DQN类
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # 折扣因子
        self.epsilon = 1.0   # 探索率
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # model input: state_size
        # model output: action_size
        # loss function: mse
        model = keras.Sequential([
            keras.layers.Dense(24, input_dim=self.state_size, activation='relu'),
            keras.layers.Dense(24, activation='relu'),
            keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            # state shape: (1, state_size)
            # action shape: (1,)    
            # reward shape: ()
            # next_state shape: (1, state_size)
            # done shape: ()
            if done:
                target_q_value = reward
            else:
                next_q_values = self.model.predict(next_state)[0]
                max_next_q_value = np.amax(next_q_values)
                target_q_value = reward + self.gamma * max_next_q_value
            
            # current_q_values shape: (1, action_size)
            current_q_values = self.model.predict(state)
            
            current_q_values[0][action] = target_q_value
            # model label: current_q_values
            self.model.fit(state, current_q_values, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def test_agent(agent, env, episodes=10):
    scores = []
    for e in range(episodes):
        state = env.reset()[0]
        state = np.reshape(state, [1, state_size])
        done = False
        score = 0
        while not done:
            action = agent.act(state)
            next_state, reward, done, _, _ = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            state = next_state
            score += 1
            if done:
                break
        scores.append(score)
        print(f"Test Episode: {e+1}/{episodes}, Score: {score}")
    print(f"Average Score: {np.mean(scores)}")

# 主程序
if __name__ == "__main__":
    env = gym.make('CartPole-v1')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    batch_size = 32
    epochs = 50  # 增加训练回合数

    # 训练阶段
    for e in range(epochs):
        state = env.reset()[0]
        state = np.reshape(state, [1, state_size])
        for time in range(50):  # 每个回合的最大步数
            action = agent.act(state)
            next_state, reward, done, _, _ = env.step(action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"episode: {e}/{500}, score: {time}, e: {agent.epsilon:.2}")
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

    # 测试阶段
    print("\nTesting the trained agent:")
    test_agent(agent, env)

    env.close()
