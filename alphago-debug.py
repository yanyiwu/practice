import numpy as np
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Simplified Go game (5x5 board)
class GoGame:
    def __init__(self):
        self.board = np.zeros((5, 5))
        self.current_player = 1

    def get_legal_moves(self):
        return [(i, j) for i in range(5) for j in range(5) if self.board[i, j] == 0]

    def make_move(self, move):
        i, j = move
        self.board[i, j] = self.current_player
        self.current_player = -self.current_player

    def is_game_over(self):
        return len(self.get_legal_moves()) == 0

    def get_winner(self):
        return np.sign(np.sum(self.board))

# Neural Network
class NeuralNetwork:
    def __init__(self):
        self.policy_network = self._build_network()
        self.value_network = self._build_network()

    def _build_network(self):
        model = Sequential([
            Dense(64, activation='relu', input_shape=(25,)),
            Dense(32, activation='relu'),
            Dense(25, activation='softmax')
        ])
        model.compile(optimizer=Adam(), loss='mse')
        return model

    def predict(self, state):
        state_flat = state.flatten()
        policy = self.policy_network.predict(state_flat.reshape(1, -1))[0]
        value = self.value_network.predict(state_flat.reshape(1, -1))[0]
        return policy, value[0]

# MCTS Node
class MCTSNode:
    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0

    def expand(self, policy):
        for move in self.game.get_legal_moves():
            child_game = GoGame()
            child_game.board = self.game.board.copy()
            child_game.current_player = self.game.current_player
            child_game.make_move(move)
            self.children.append(MCTSNode(child_game, self, move))

    def select_child(self):
        return max(self.children, key=lambda c: c.value / (c.visits + 1) + 0.5 * np.sqrt(self.visits) / (c.visits + 1))

# Simplified AlphaGo
class SimpleAlphaGo:
    def __init__(self):
        self.nn = NeuralNetwork()

    def select_move(self, game, num_simulations=100):
        root = MCTSNode(game)
        for _ in range(num_simulations):
            node = root
            while node.children:
                node = node.select_child()
            
            policy, value = self.nn.predict(node.game.board)
            node.expand(policy)
            
            while node:
                node.visits += 1
                node.value += value
                node = node.parent

        return max(root.children, key=lambda c: c.visits).move

# Demonstration game
def play_game():
    game = GoGame()
    ai = SimpleAlphaGo()

    while not game.is_game_over():
        if game.current_player == 1:
            move = ai.select_move(game)
        else:
            move = random.choice(game.get_legal_moves())
        game.make_move(move)
        print(game.board)
        print("---")

    winner = game.get_winner()
    if winner == 1:
        print("AI wins!")
    elif winner == -1:
        print("Random player wins!")
    else:
        print("It's a draw!")

play_game()
