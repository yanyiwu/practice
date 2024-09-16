import numpy as np
import tensorflow as tf
from tensorflow import keras
import random

# Game environment
class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1

    def get_valid_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def make_move(self, move):
        if isinstance(move, int):
            i, j = move // 3, move % 3
        else:
            i, j = move
        self.board[i, j] = self.current_player
        self.current_player = -self.current_player

    def check_winner(self):
        for player in [1, -1]:
            if any(np.all(self.board == player, axis=0)) or \
               any(np.all(self.board == player, axis=1)) or \
               np.all(np.diag(self.board) == player) or \
               np.all(np.diag(np.fliplr(self.board)) == player):
                return player
        if np.all(self.board != 0):
            return 0
        return None

    def get_state(self):
        return self.board.copy(), self.current_player

# Neural Network
class NeuralNetwork:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = keras.Sequential([
            keras.layers.Input(shape=(3, 3, 2)),
            keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
            keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(9 + 1)  # 9 move probabilities + 1 value
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def predict(self, state):
        board, player = state
        x = np.stack([board == player, board == -player], axis=-1).astype(np.float32)
        x = np.expand_dims(x, 0)
        prediction = self.model.predict(x)[0]
        move_probs, value = prediction[:9], prediction[9]
        return move_probs, value

# MCTS
class MCTS:
    def __init__(self, game, nn, num_simulations):
        self.game = game
        self.nn = nn
        self.num_simulations = num_simulations

    def search(self, state):
        root = MCTSNode(state)
        for _ in range(self.num_simulations):
            node = root
            search_path = [node]

            # 选择
            while node.expanded():
                node = node.select_child()
                search_path.append(node)

            # 扩展
            if not node.expanded():
                move_probs, value = self.nn.predict(node.state)
                valid_moves = self.game.get_valid_moves()
                move_probs = [move_probs[i * 3 + j] if (i, j) in valid_moves else 0 
                              for i in range(3) for j in range(3)]
                move_probs /= np.sum(move_probs)
                node.expand(move_probs)
            
            # 模拟
            if len(search_path) > 1:
                parent = search_path[-2]
                move = node.move
                self.game.board, self.game.current_player = parent.state
                self.game.make_move(move)
                game_result = self.game.check_winner()
            else:
                game_result = self.game.check_winner()

            # 如果游戏未结束，使用神经网络的预测值
            if game_result is None:
                _, value = self.nn.predict(node.state)
            else:
                value = game_result

            # 回传
            self.backpropagate(search_path, value, self.game.current_player)

        return root

    def backpropagate(self, search_path, value, current_player):
        for node in reversed(search_path):
            if isinstance(value, (int, float)):  # 确保 value 是数值
                node.value_sum += value if node.state[1] == current_player else -value
            node.visit_count += 1

class MCTSNode:
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.move = move  # 这里的 move 可能是整数
        self.parent = parent
        self.children = []
        self.visit_count = 0
        self.value_sum = 0
        self.prior = 0

    def expanded(self):
        return len(self.children) > 0

    def select_child(self):
        c_puct = 1.0
        return max(self.children, key=lambda child: child.get_ucb(c_puct))

    def expand(self, move_probs):
        for move, prob in enumerate(move_probs):
            if prob > 0:
                child_state = (self.state[0].copy(), -self.state[1])
                i, j = move // 3, move % 3
                child_state[0][i, j] = self.state[1]
                child = MCTSNode(child_state, move=move, parent=self)
                child.prior = prob
                self.children.append(child)

    def get_ucb(self, c_puct):
        q_value = self.value_sum / self.visit_count if self.visit_count > 0 else 0
        return q_value + c_puct * self.prior * np.sqrt(self.parent.visit_count) / (1 + self.visit_count)

# AlphaZero
class AlphaZero:
    def __init__(self, game, nn):
        self.game = game
        self.nn = nn
        self.mcts = MCTS(game, nn, num_simulations=100)

    def self_play(self):
        state = self.game.get_state()
        states, mcts_probs, current_players = [], [], []

        while True:
            root = self.mcts.search(state)
            mcts_prob = [0] * 9
            for child in root.children:
                mcts_prob[child.move] = child.visit_count
            mcts_prob = np.array(mcts_prob, dtype=np.float32)
            if np.sum(mcts_prob) > 0:
                mcts_prob /= np.sum(mcts_prob)
            else:
                # 如果所有概率都为0，使用均匀分布
                mcts_prob = np.ones(9) / 9

            states.append(state)
            mcts_probs.append(mcts_prob)
            current_players.append(self.game.current_player)

            temperature = 1.0
            move = np.random.choice(9, p=mcts_prob ** (1 / temperature))
            self.game.make_move((move // 3, move % 3))

            state = self.game.get_state()
            winner = self.game.check_winner()

            if winner is not None:
                return states, mcts_probs, current_players, winner

    def train(self, num_iterations):
        for iteration in range(num_iterations):
            states, mcts_probs, current_players, winner = self.self_play()
            
            for i in range(len(states)):
                state = states[i]
                mcts_prob = mcts_probs[i]
                current_player = current_players[i]

                board, player = state
                x = np.stack([board == player, board == -player], axis=-1).astype(np.float32)
                x = np.expand_dims(x, 0)

                y = np.zeros((1, 10), dtype=np.float32)
                y[0, :9] = mcts_prob
                y[0, 9] = 1 if winner == current_player else -1 if winner == -current_player else 0

                self.nn.model.fit(x, y, verbose=0)

            print(f"Iteration {iteration + 1}/{num_iterations} completed")

# Main
game = TicTacToe()
nn = NeuralNetwork()
alphazero = AlphaZero(game, nn)

# Train for 10 iterations (you may want to increase this for better results)
alphazero.train(10)

# Play a game against a random player
game = TicTacToe()
while True:
    if game.current_player == 1:
        state = game.get_state()
        root = alphazero.mcts.search(state)
        if not root.children:
            print("No valid moves found. Ending the game.")
            break
        mcts_prob = [child.visit_count for child in root.children]
        if all(prob == 0 for prob in mcts_prob):
            print("All move probabilities are zero. Choosing a random move.")
            chosen_child = random.choice(root.children)
        else:
            chosen_child = root.children[np.argmax(mcts_prob)]
        move = chosen_child.move
        game.make_move((move // 3, move % 3))  
    else:
        valid_moves = game.get_valid_moves()
        move = random.choice(valid_moves)
        game.make_move(move)
    
    print(game.board)
    print()
    
    winner = game.check_winner()
    if winner is not None:
        if winner == 1:
            print("AlphaZero wins!")
        elif winner == -1:
            print("Random player wins!")
        else:
            print("It's a draw!")
        break
