import gym
import numpy as np
import matplotlib.pyplot as plt

# Create CartPole environment
env = gym.make('CartPole-v1')

# Discretize the continuous state space
# return a tuple of discretized state, length is 4 (cart position, cart velocity, pole angle, pole velocity at tip)
def discretize_state(state_dict):
    state = state_dict['obs'] if isinstance(state_dict, dict) else state_dict
    discretized = []
    for feature in state:
        discretized.append(np.digitize(feature, bins=[-0.5, 0.5]))
    return tuple(discretized)

# Initialize Q-table with zeros
DISCRETE_OS_SIZE = [5] * 2 + [3] * 2
q_table = np.zeros(DISCRETE_OS_SIZE + [env.action_space.n])
# q_table shape: (5, 5, 3, 3, 2), total states: 5 * 5 * 3 * 3 * 2 = 450

# Hyperparameters
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 50000
EPSILON = 0.1  # 设置一个固定的探索率，例如 10%

# For statistics
STATS_EVERY = 1000
ep_rewards = []

# Training loop
for episode in range(EPISODES):
    state = discretize_state(env.reset()[0])
    done = False
    episode_reward = 0

    while not done:
        # Epsilon-greedy action selection
        if np.random.random() > EPSILON:
            action = np.argmax(q_table[state])
        else:
            action = np.random.randint(0, env.action_space.n)
        
        new_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        new_state = discretize_state(new_state)
        episode_reward += reward

        # Q-learning update
        old_q = q_table[state + (action,)]
        next_max_q = np.max(q_table[new_state])
        new_q = (1 - LEARNING_RATE) * old_q + LEARNING_RATE * (reward + DISCOUNT * next_max_q)
        q_table[state + (action,)] = new_q

        state = new_state

    # Keep track of rewards
    ep_rewards.append(episode_reward)

    # Print statistics periodically
    if episode % STATS_EVERY == 0:
        average_reward = sum(ep_rewards[-STATS_EVERY:]) / STATS_EVERY
        print(f"Episode: {episode}, Avg Reward: {average_reward:.2f}, Epsilon: {EPSILON:.2f}")

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
    state = discretize_state(env.reset()[0])
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
    
    print(f"Test Episode: {episode}, Reward: {episode_reward}")

env.close()
