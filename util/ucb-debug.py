import math
import random

def ucb1(node, parent_visits):
    """
    Calculate the UCB1 value for a node.

    The UCB1 (Upper Confidence Bound 1) algorithm balances exploration and exploitation
    in the selection phase of Monte Carlo Tree Search.

    Args:
        node: The node for which to calculate the UCB1 value.
        parent_visits: The number of visits to the parent node.

    Returns:
        float: The UCB1 value for the node.
    """
    if node.visits == 0:
        return float('inf')  # Ensure unvisited nodes are explored first
    
    # UCB1 formula: (node value / node visits) + C * sqrt(ln(parent visits) / node visits)
    exploitation = node.value / node.visits
    exploration = math.sqrt(2 * math.log(parent_visits) / node.visits)
    
    return exploitation + exploration

class Node:
    def __init__(self, value=0, visits=0):
        self.value = value
        self.visits = visits

def demo_ucb1():
    """
    Demonstrate the UCB1 algorithm with a simple example.
    """
    parent_visits = 0
    # Create a list of 5 nodes with random initial values
    nodes = [Node(value=random.randint(1, 10)) for _ in range(5)]

    print("Initial node values:")
    for i, node in enumerate(nodes):
        print(f"Node {i + 1}: Value = {node.value}, Visits = {node.visits}")

    # Simulate 100 iterations
    for _ in range(100):
        # Select node with highest UCB1 value
        selected_node = max(nodes, key=lambda n: ucb1(n, parent_visits))
        selected_node.visits += 1
        selected_node.value += random.randint(0, 10)  # Simulate reward
        parent_visits += 1

    print("\nFinal node states and UCB1 values:")
    for i, node in enumerate(nodes):
        ucb_value = ucb1(node, parent_visits)
        print(f"Node {i + 1}: Value = {node.value}, Visits = {node.visits}, UCB1 = {ucb_value:.4f}")

    # Find the node with the highest value
    best_node = max(nodes, key=lambda n: n.value)
    print(f"\nBest node: Value = {best_node.value}, Visits = {best_node.visits}")

if __name__ == "__main__":
    demo_ucb1()

