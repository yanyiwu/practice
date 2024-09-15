import math
import time
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

def ucb1(node):
    if node.visits == 0:
        return float('inf')
    return node.wins / node.visits + 1.41 * math.sqrt(math.log(node.parent.visits) / node.visits)

def select_child_ucb1(node):
    return max(node.children, key=ucb1)

def expand(node):
    possible_moves = get_possible_moves(node.state)
    for move in possible_moves:
        new_state = make_move(node.state, move, 'X')
        child = Node(new_state, node)
        node.children.append(child)
    return random.choice(node.children)

def simulate(node, starting_player='O'):
    state = node.state[:]
    current_player = starting_player
    while True:
        possible_moves = get_possible_moves(state)
        if not possible_moves:
            return 0  # Draw
        move = random.choice(possible_moves)
        state[move] = current_player
        if is_win(state, current_player):
            return 1 if current_player == 'X' else -1
        current_player = 'O' if current_player == 'X' else 'X'

def backpropagate(node, result):
    while node:
        node.visits += 1
        node.wins += result
        node = node.parent
        result = -result

def mcts(state, max_time):
    root = Node(state)
    end_time = time.time() + max_time
    iteration = 0
    while time.time() < end_time:
        node = root
        # Selection
        while node.children and not is_terminal(node.state):
            node = select_child_ucb1(node)
        
        # Expansion
        if not is_terminal(node.state):
            expand(node)
            node = random.choice(node.children)
        
        # Simulation
        result = simulate(node)
        
        # Backpropagation
        backpropagate(node, result)

        # Print tree stats every 100 iterations
        iteration += 1
        if iteration % 1 == 0:
            total_nodes, max_depth = get_tree_stats(root)
            print(f"\nIteration {iteration}:")
            print(f"Total nodes: {total_nodes}")
            print(f"Max depth: {max_depth}")

    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.state

def get_tree_stats(node):
    def dfs(n, current_depth):
        if not n.children:
            return 1, current_depth
        
        count = 1
        max_depth = current_depth
        for child in n.children:
            child_count, child_depth = dfs(child, current_depth + 1)
            count += child_count
            max_depth = max(max_depth, child_depth)
        
        return count, max_depth

    total_nodes, max_depth = dfs(node, 0)
    return total_nodes, max_depth

def is_terminal(state):
    return is_win(state, 'X') or is_win(state, 'O') or '-' not in state

def is_win(state, player):
    # Check rows, columns, and diagonals
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    return any(all(state[i] == player for i in combo) for combo in win_combinations)

def evaluate(state):
    if is_win(state, 'X'):
        return 1
    elif is_win(state, 'O'):
        return -1
    else:
        return 0

def get_possible_moves(state):
    return [i for i, cell in enumerate(state) if cell == '-']

def make_move(state, move, player):
    new_state = state[:]
    new_state[move] = player  # Use the player parameter, defaulting to 'X'
    return new_state

def make_random_move(state, player):
    possible_moves = get_possible_moves(state)
    if possible_moves:
        move = random.choice(possible_moves)
        state[move] = player

# Test the MCTS algorithm
initial_state = ['X', '-', '-',
                '-', 'X', '-',
                '-', '-', '-']
initial_state = ['-', '-', '-',
                '-', '-', '-',
                '-', '-', '-']
best_state = mcts(initial_state, max_time=100)
print("Initial state:", initial_state)
print("Best state found:", best_state)