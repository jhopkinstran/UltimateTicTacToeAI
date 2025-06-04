

class SimpleRLAgent:
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder

    def get_action(self, game_state):
        state_encoding = self.encoder.encode(game_state)
    