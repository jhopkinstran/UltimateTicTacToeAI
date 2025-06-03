import random

class RandomAgent:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    def get_action(self, game_state):
        actions = game_state.get_valid_actions()
        return random.choice(actions)