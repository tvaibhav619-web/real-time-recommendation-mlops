class Bandit:
    def __init__(self):
        self.values = {}

    def update(self, action, reward):
        self.values[action] = self.values.get(action, 0) + reward
