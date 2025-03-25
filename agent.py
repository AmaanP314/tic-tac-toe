import numpy as np
import random

class TicTacToeEnv:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.current_player = 1  # Player 1 is X (1), Player -1 is O (-1)

    def reset(self):
        self.board = np.zeros((3, 3))
        self.current_player = 1
        return self.board

    def make_move(self, row, col):
        if self.board[row, col] == 0:  # Valid move
            self.board[row, col] = self.current_player
            if self.check_winner():
                return self.board, self.current_player, True  # Game won by current player
            elif self.check_draw():
                return self.board, 0, True  # Draw
            else:
                self.current_player = -self.current_player  # Switch player
                return self.board, 0, False  # Game continues
        return self.board, 0, False  # Invalid move


    def check_winner(self):
        for i in range(3):
            if np.all(self.board[i, :] == self.current_player) or np.all(self.board[:, i] == self.current_player):
                return True
        if self.board[0, 0] == self.current_player == self.board[1, 1] == self.board[2, 2]:
            return True
        if self.board[0, 2] == self.current_player == self.board[1, 1] == self.board[2, 0]:
            return True
        return False

    def check_draw(self):
        return np.all(self.board != 0)

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.q_table = {}  # Q-table to store state-action values
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def get_state_key(self, state):
        return str(state.reshape(9))  # Convert board state to a string key

    # def choose_action(self, state, available_actions):
    #     # Exploration vs Exploitation
    #     if np.random.rand() < self.exploration_rate:
    #         return random.choice([row * 3 + col for row, col in available_actions])  # Convert (row, col) to action index
    #     else:
    #         state_key = self.get_state_key(state)
    #         q_values = self.q_table.get(state_key, np.zeros(9))
    #         # Choose the best action among the available ones
    #         available_action_indices = [action[0] * 3 + action[1] for action in available_actions]
    #         action = max(available_action_indices, key=lambda x: q_values[x])
    #         return action
    # def choose_action(self, state, available_actions):
    #     if np.random.rand() < self.exploration_rate:
    #         # Select a random action index (from 0-8)
    #         return random.choice([row * 3 + col for row, col in available_actions])
    #     else:
    #         state_key = self.get_state_key(state)
    #         q_values = self.q_table.get(state_key, np.zeros(9))
    #         return np.argmax(q_values)
    def choose_action(self, state, available_actions):
        if np.random.rand() < self.exploration_rate:
            # Choose randomly from available actions
            action = random.choice(available_actions)
            print(f"Randomly chosen action: {action}")
        else:
            # Exploit: choose the action with the highest Q-value
            state_key = self.get_state_key(state)
            q_values = self.q_table.get(state_key, np.zeros(9))
            action = np.argmax(q_values)
            print(f"Exploiting chosen action: {action}")

        # Ensure the chosen action is in available_actions
        if action not in available_actions:
            print(f"Action {action} not in available actions {available_actions}")
            action = random.choice(available_actions)  # Fallback to random action if invalid

        return action

    def update_q_values(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(9)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(9)

        best_next_action = np.argmax(self.q_table[next_state_key])
        # Q-value update using the Bellman equation
        self.q_table[state_key][action] = self.q_table[state_key][action] + \
            self.learning_rate * (reward + self.discount_factor * self.q_table[next_state_key][best_next_action] - self.q_table[state_key][action])

        self.exploration_rate *= self.exploration_decay  # Decaying exploration rate

# Training with self-play
env = TicTacToeEnv()
agent = QLearningAgent()

# for episode in range(10000):  # Number of games for training
#     state = env.reset()
#     done = False
#     while not done:
#         available_actions = np.argwhere(state == 0)  # Get empty cells (row, col pairs)
#         available_actions = [(x[0], x[1]) for x in available_actions]  # List of available (row, col) pairs
#         action_idx = agent.choose_action(state, available_actions)
#         row, col = divmod(action_idx, 3)  # Correctly converting action index to (row, col)
        
#         next_state, reward, done = env.make_move(row, col)

#         if done:
#             # If game is won or drawn, assign final reward
#             agent.update_q_values(state, action_idx, reward, next_state)
#         else:
#             # Continue updating Q-values for intermediate states
#             agent.update_q_values(state, action_idx, 0, next_state)

#         state = next_state

#     if episode % 1000 == 0:
#         print(f"Episode {episode}, Exploration Rate: {agent.exploration_rate}")

for episode in range(1000):  # Number of games for training
    state = env.reset()
    done = False
    print(f"Episode {episode}: Starting new game")
    while not done:
        available_actions = np.argwhere(state == 0).flatten()  # Get empty cells as 1D array
        print(f"Available actions: {available_actions}")

        if len(available_actions) == 0:
            print("No available actions. Something went wrong.")
            break
        
        action_idx = agent.choose_action(state, available_actions)
        print(f"Chosen action index: {action_idx}")

        row, col = divmod(action_idx, 3)  # Convert action index to row, col
        print(f"Chosen action: (row: {row}, col: {col})")

        next_state, reward, done = env.make_move(row, col)
        print(f"Move result - Reward: {reward}, Done: {done}")

        # Update Q-values
        agent.update_q_values(state, action_idx, reward, next_state)
        
        state = next_state

        if done:
            if reward == 1:
                print(f"Game won by player {env.current_player}")
            elif reward == 0:
                print("Game ended in a draw")
            else:
                print("Game in progress")

    if episode % 100 == 0:
        print(f"Episode {episode}, Exploration Rate: {agent.exploration_rate}")


print("Training Complete!")
