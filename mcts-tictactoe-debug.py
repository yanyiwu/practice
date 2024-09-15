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

def uct(node):
    if node.visits == 0:
        return float('inf')
    return node.wins / node.visits + 1.41 * math.sqrt(math.log(node.parent.visits) / node.visits)

def select_child(node):
    best_score = -float('inf')
    best_child = None
    for child in node.children:
        score = uct(child)
        if score > best_score:
            best_score = score
            best_child = child
    return best_child

def expand(node):
    possible_moves = get_possible_moves(node.state)
    for move in possible_moves:
        new_state = make_move(node.state, move)
        child = Node(new_state, node)
        node.children.append(child)
    return random.choice(node.children)

def simulate(node):
    state = node.state[:]
    while True:
        possible_moves = get_possible_moves(state)
        if not possible_moves:
            return 0
        make_random_move(state)
        if is_win(state, 'X'):
            return 1
        if is_win(state, 'O'):
            return -1

def backpropagate(node, result):
    while node:
        node.visits += 1
        node.wins += result
        node = node.parent
        result = -result

def mcts(state, max_time):
    root = Node(state)
    end_time = time.time() + max_time
    while time.time() < end_time:
        node = root
        while node.children:
            node = select_child(node)
        if is_terminal(node.state):
            result = evaluate(node.state)
            backpropagate(node, result)
            continue
        if not node.children:
            expand(node)
        child = random.choice(node.children)
        result = simulate(child)
        backpropagate(child, result)
    
    best_child = None
    best_score = -float('inf')
    for child in root.children:
        score = child.wins / child.visits
        if score > best_score:
            best_score = score
            best_child = child
    return best_child.state


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

def make_move(state, move):
    new_state = state[:]
    new_state[move] = 'X'  # Assuming 'X' is the current player
    return new_state

def make_random_move(state):
    possible_moves = get_possible_moves(state)
    if possible_moves:
        move = random.choice(possible_moves)
        state[move] = 'O'  # Assuming 'O' is the opponent

# Test the MCTS algorithm
initial_state = ['X', '-', '-',
                '-', 'X', '-',
                '-', '-', '-']
best_state = mcts(initial_state, max_time=5)
print("Initial state:", initial_state)
print("Best state found:", best_state)