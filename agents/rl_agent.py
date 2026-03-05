import random

class RLAgent:

    def __init__(self):
        self.q_table = {}
        self.actions = ["OPTIMIZE_PATH", "LOAD_BALANCE", "NORMAL_OPERATION"]

    def get_state(self, latency, bandwidth):
        if latency > 100:
            return "HIGH_LATENCY"
        elif bandwidth < 50:
            return "LOW_BANDWIDTH"
        else:
            return "NORMAL"

    def choose_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0, 0, 0]

        # simple epsilon-greedy
        if random.random() < 0.2:
            action = random.choice(self.actions)
        else:
            q_values = self.q_table[state]
            action = self.actions[q_values.index(max(q_values))]

        return action

    def update_q(self, state, action, reward):
        lr = 0.1
        gamma = 0.9

        action_index = self.actions.index(action)

        if state not in self.q_table:
            self.q_table[state] = [0, 0, 0]

        old_value = self.q_table[state][action_index]
        new_value = old_value + lr * (reward + gamma * max(self.q_table[state]) - old_value)

        self.q_table[state][action_index] = new_value