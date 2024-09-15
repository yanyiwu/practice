import random
import math

class GuessNumberGame:
    def __init__(self):
        self.target = random.randint(1, 100)
        self.max_steps = 10

    def guess(self, number):
        if number == self.target:
            return 0  # 正确
        elif number < self.target:
            return -1  # 低了
        else:
            return 1  # 高了

    def is_terminal(self, state):
        return state['steps'] >= self.max_steps or state['last_guess'] == self.target

    def get_reward(self, state):
        return 1 if state['last_guess'] == self.target else 0

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
        if node.parent is None:
            # 对于根节点，使用节点自身的访问次数
            node = max(node.children, key=lambda c: ucb1(c, node.visits))
        else:
            node = max(node.children, key=lambda c: ucb1(c, node.parent.visits))
    return node

def expand(node, game):
    if game.is_terminal(node.state):
        return node
    for guess in range(1, 101):
        if guess not in [c.state['last_guess'] for c in node.children]:
            new_state = node.state.copy()
            new_state['steps'] += 1
            new_state['last_guess'] = guess
            new_node = Node(new_state, parent=node)
            node.children.append(new_node)
            return new_node
    return node

def simulate(game, state):
    while not game.is_terminal(state):
        guess = random.randint(1, 100)
        result = game.guess(guess)
        state['steps'] += 1
        state['last_guess'] = guess
        if result == 0:
            break
    return game.get_reward(state)

def backpropagate(node, reward):
    while node:
        node.visits += 1
        node.value += reward
        node = node.parent

def mcts(game, num_iterations):
    root = Node({'steps': 0, 'last_guess': None})
    for _ in range(num_iterations):
        node = select(root)
        node = expand(node, game)
        reward = simulate(game, node.state.copy())
        backpropagate(node, reward)
    
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.state['last_guess']

def monte_carlo(game, num_simulations):
    best_guess = None
    best_score = float('-inf')

    for guess in range(1, 101):
        total_reward = 0
        for _ in range(num_simulations):
            state = {'steps': 0, 'last_guess': None}
            while not game.is_terminal(state):
                result = game.guess(guess)
                state['steps'] += 1
                state['last_guess'] = guess
                if result == 0:
                    break
                guess = random.randint(1, 100)
            total_reward += game.get_reward(state)
        
        average_reward = total_reward / num_simulations
        if average_reward > best_score:
            best_score = average_reward
            best_guess = guess

    return best_guess

game = GuessNumberGame()
print(f"Target number: {game.target}")

mc_guess = monte_carlo(game, 1000)
print(f"Monte Carlo guess: {mc_guess}")

mcts_guess = mcts(game, 1000)
print(f"MCTS guess: {mcts_guess}")

print(f"MC result: {game.guess(mc_guess)}")
print(f"MCTS result: {game.guess(mcts_guess)}")
