from board import UltimateBoard
from game_state import GameState
from encoders.flat_encoder import FlatEncoder
from encoders.base_encoder import StateEncoder

class UltimateTicTacToeEnv:
    def __init__(self, ruleset="default"):
        self.ruleset = ruleset
        self.agent_player = 1
        self.state = GameState(UltimateBoard(), ruleset=self.ruleset)

    def reset(self):
        self.state = GameState(UltimateBoard(), ruleset=self.ruleset)
        return self.state()

    def step(self, action: tuple[int, int, int, int]):
        self.state.make_move(*action)
        reward = self.compute_reward()
        done = self.state.game_over
        return self.state, reward, done
    
    def get_valid_actions(self):
        return self.state.get_valid_actions()
    
    def compute_reward(self) -> float:
        if not self.state.game_over:
            return 0.0
        elif self.state.winner == self.agent_player:
            return 1.0
        elif self.state.winner == 0:
            return 0.0
        else:
            return -1.0
