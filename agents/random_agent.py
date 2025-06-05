import random
from agent import Agent

class RandomAgent(Agent):
    def __init__(self, seed=None):
        super().__init__()
        if seed is not None:
            random.seed(seed)

    def get_action(self, game_state):
        actions = game_state.get_valid_actions()
        return random.choice(actions)