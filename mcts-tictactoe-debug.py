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
    return node.wins / node.visits + 10 * math.sqrt(math.log(node.parent.visits) / node.visits)

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
    print_board(state)
    current_player = starting_player
    while True:
        possible_moves = get_possible_moves(state)
        if not possible_moves:
            return 0  # Draw
        move = random.choice(possible_moves)
        state[move] = current_player
        print_board(state)
        if is_win(state, current_player):
            return 1 if current_player == 'X' else -1
        current_player = 'O' if current_player == 'X' else 'X'

def backpropagate(node, result):
    while node:
        node.visits += 1
        node.wins += result
        node = node.parent
        result = -result

def mcts(state, max_iterations):
    root = Node(state)
    for iteration in range(max_iterations):
        node = root
        # Selection
        while node.children and not is_terminal(node.state):
            node = select_child_ucb1(node)
        
        # Expansion
        if not is_terminal(node.state):
            node = expand(node)
        
        # Simulation
        result = simulate(node)
        
        # Backpropagation
        backpropagate(node, result)

        print_tree(node)

        # Print tree stats every 100 iterations
        iteration += 1
        if iteration % 1 == 0:
            total_nodes, max_depth = get_tree_stats(root)
            print(f"\nIteration {iteration}:")
            print(f"Total nodes: {total_nodes}")
            print(f"Max depth: {max_depth}")

    print("\nFinal children statistics:")
    print_children_stats(root)

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

def print_children_stats(node):
    if not node.children:
        print("This node has no children.")
        return

    total_visits = sum(child.visits for child in node.children)
    total_wins = sum(child.wins for child in node.children)
    
    print(f"Total visits to children: {total_visits}")
    print(f"Total wins of children: {total_wins}")
    print("Children statistics:")
    
    for i, child in enumerate(node.children):
        move = get_move_from_states(node.state, child.state)
        visit_percentage = (child.visits / total_visits) * 100 if total_visits > 0 else 0
        win_rate = (child.wins / child.visits) * 100 if child.visits > 0 else 0
        print(f"Child {i+1} (Move: {move}): "
              f"{child.visits} visits ({visit_percentage:.2f}%), "
              f"{child.wins} wins, "
              f"Win rate: {win_rate:.2f}%")

def get_move_from_states(parent_state, child_state):
    for i in range(len(parent_state)):
        if parent_state[i] != child_state[i]:
            return i
    return None  # This should not happen in a valid game

# Completely empty board
initial_state_empty = ['-', '-', '-',
                       '-', '-', '-',
                       '-', '-', '-']

# X starts, playing in the center
initial_state_center = ['-', '-', '-',
                        '-', 'X', '-',
                        '-', '-', '-']

# Mid-game state
initial_state_midgame = ['X', 'O', '-',
                         '-', 'X', '-',
                         'O', '-', '-']

# State where X has a chance to win
initial_state_x_winning = ['X', 'X', '-',
                           'O', 'O', '-',
                           '-', '-', '-']

# State where O has a chance to win
initial_state_o_winning = ['O', '-', 'X',
                           'X', 'O', '-',
                           '-', '-', 'X']

# State close to a draw
initial_state_near_draw = ['X', 'O', 'X',
                           'O', 'X', '-',
                           'O', 'X', 'O']

# Test function
def test_mcts(initial_state, max_iterations=1000):
    print("Initial state:")
    print_board(initial_state)
    best_state = mcts(initial_state, max_iterations)
    print("\nBest move found:")
    print_board(best_state)
    print("\n" + "="*20 + "\n")

# Helper function to print the board
def print_board(state):
    print("\n" + "="*20 + "\n")
    for i in range(0, 9, 3):
        print(" ".join(state[i:i+3]))
    print("\n" + "="*20 + "\n")

def print_tree(node, prefix="", is_last=True, max_depth=3):
    if max_depth < 0:
        return

    # Print current node
    state_str = "".join(node.state)
    node_info = f"{state_str} (V:{node.visits}, W:{node.wins:.1f})"
    print(f"{prefix}{'└── ' if is_last else '├── '}{node_info}")

    # Prepare prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")

    # Print children
    if node.children:
        children = list(node.children)
        for i, (move, child) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            print(f"{child_prefix}│")
            print(f"{child_prefix}Move {move}:")
            print_tree(child, child_prefix, is_last_child, max_depth - 1)
    elif max_depth > 0:
        print(f"{child_prefix}(Leaf node)")


# List of all test states
test_states = [
    initial_state_empty,
    initial_state_center,
    initial_state_midgame,
    initial_state_x_winning,
    initial_state_o_winning,
#    initial_state_near_draw,
]

# Run the tests in a loop
for i, state in enumerate(test_states):
    print(f"\nTest case {i}:")
    print_board(state)
    test_mcts(state, max_iterations=1000)  # 你可以根据需要调整迭代次数

