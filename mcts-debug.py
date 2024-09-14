import math
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

def ucb1(node, parent_visits):
    if node.visits == 0:
        return float('inf')
    return node.value / node.visits + math.sqrt(2 * math.log(parent_visits) / node.visits)

def select(node):
    while node.children:
        node = max(node.children, key=lambda c: ucb1(c, node.visits))
    return node

def expand(node, game):
    if game.is_terminal(node.state):
        return node
    for action in game.get_actions(node.state):
        if action not in [c.state for c in node.children]:
            new_state = game.get_next_state(node.state, action)
            new_node = Node(new_state, parent=node)
            node.children.append(new_node)
            return new_node
    return node

def simulate(game, state):
    while not game.is_terminal(state):
        action = random.choice(game.get_actions(state))
        state = game.get_next_state(state, action)
    return game.get_reward(state)

def backpropagate(node, reward):
    while node:
        node.visits += 1
        node.value += reward
        node = node.parent

def mcts(game, root_state, num_iterations):
    root = Node(root_state)
    for _ in range(num_iterations):
        node = select(root)
        node = expand(node, game)
        reward = simulate(game, node.state)
        backpropagate(node, reward)
    return max(root.children, key=lambda c: c.visits).state

class SimpleGame:
    def is_terminal(self, state):
        return state >= 10

    def get_actions(self, state):
        return [1, 2]

    def get_next_state(self, state, action):
        return state + action

    def get_reward(self, state):
        return 1 if state == 10 else 0

game = SimpleGame()
initial_state = 0
best_action = mcts(game, initial_state, 1000)
print(f"Best action: {best_action}")
