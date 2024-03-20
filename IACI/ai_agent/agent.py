# ai_agent/agent.py

import random

from environment.simulator import VirtualComputerEnvironment

# ai_agent/agent.py (Q-learning Conceptual Adaptation)

import numpy as np

class QLearningAgent:
    def __init__(self, environment, actions, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.environment = environment
        self.q_table = np.zeros((len(environment.states), len(actions)))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.actions = actions

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            # Exploration: choose a random action
            return np.random.choice(self.actions)
        else:
            # Exploitation: choose the best action from Q-table
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])  # Best next action
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

class ComputerInteractionAgent:
    def __init__(self):
        self.environment = VirtualComputerEnvironment()
        self.reward = 0  # Initial reward

    def choose_action(self):
        """Randomly chooses an action from the available actions."""
        actions = ['list_files', 'open_file', 'close_file']
        return random.choice(actions)

    def perform_action(self, action):
        """Performs an action and updates the environment and reward."""
        if action == 'list_files':
            self.environment.list_files()
        elif action == 'open_file':
            # Simplification: Assuming a file named 'example.txt' exists
            self.environment.open_file('example.txt')
            self.reward += 1  # Reward for opening a file
        elif action == 'close_file':
            self.environment.close_file()
            self.reward -= 1  # Penalty for closing a file (to encourage exploration)

    def run_episode(self):
        """Runs one episode of interaction with the environment."""
        for _ in range(10):  # Limit the episode to 10 actions for simplicity
            action = self.choose_action()
            self.perform_action(action)
            print(f"Current Reward: {self.reward}")

if __name__ == "__main__":
    agent = ComputerInteractionAgent()
    agent.run_episode()
