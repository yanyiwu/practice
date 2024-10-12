import gym
import numpy as np
import matplotlib.pyplot as plt

# Create CartPole environment
env = gym.make('CartPole-v1')

# Discretize the continuous state space
def discretize_state(state_dict):
    state = state_dict['obs'] if isinstance(state_dict, dict) else state_dict
    discretized = []
    for feature in state:
        discretized.append(np.digitize(feature, bins=[-0.5, 0.5]))
    return tuple(discretized)

# Initialize Q-table with zeros
DISCRETE_OS_SIZE = [5] * 2 + [3] * 2
q_table = np.zeros(DISCRETE_OS_SIZE + [env.action_space.n])

# Hyperparameters
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 50000
epsilon = 1.0  # Exploration rate
EPSILON_DECAY = 0.99995
MIN_EPSILON = 0.01

# For statistics
STATS_EVERY = 1000
ep_rewards = []

# Training loop
for episode in range(EPISODES):
    state, _ = env.reset()  # Unpack the tuple returned by env.reset()
    state = discretize_state(state)
    done = False
    episode_reward = 0

    while not done:
        # Epsilon-greedy action selection
        if np.random.random() > epsilon:
            action = np.argmax(q_table[state])
        else:
            action = np.random.randint(0, env.action_space.n)
        
        new_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        new_state = discretize_state(new_state)
        episode_reward += reward

        # Q-learning update
        if not done:
            max_future_q = np.max(q_table[new_state])
            current_q = q_table[state + (action,)]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[state + (action,)] = new_q
        else:
            q_table[state + (action,)] = 0  # Terminal state

        state = new_state

    # Decay epsilon
    epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)

    # Keep track of rewards
    ep_rewards.append(episode_reward)

    # Print statistics periodically
    if episode % STATS_EVERY == 0:
        average_reward = sum(ep_rewards[-STATS_EVERY:]) / STATS_EVERY
        print(f"Episode: {episode}, Avg Reward: {average_reward:.2f}, Epsilon: {epsilon:.2f}")

env.close()

# Plot results
plt.plot(range(EPISODES), ep_rewards)
plt.title('Rewards over Episodes')
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.show()

# Test the trained agent
test_episodes = 10
for episode in range(test_episodes):
    state, _ = env.reset()  # Unpack the tuple returned by env.reset()
    state = discretize_state(state)
    done = False
    episode_reward = 0
    
    while not done:
        env.render()
        action = np.argmax(q_table[state])
        new_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        new_state = discretize_state(new_state)
        episode_reward += reward
        state = new_state
    
    print(f"Test Episode: {episode + 1}, Reward: {episode_reward}")

env.close()
