# Encoder stores the 81 squares, 9 win states, and player turn
from base_encoder import StateEncoder
import numpy as np

class MinEncoder(StateEncoder):
    def encode(self, game_state):
        board = game_state.board
        flat_grid = []

        for ult_r in range(3):
            for ult_c in range(3):
                mini = board.get_mini_board(ult_r, ult_c)
                for r in range(3):
                    for c in range(3):
                        flat_grid.append(mini.grid[r][c])

        flat_grid.append(game_state.player_turn)
        return np.array(flat_grid, dtype=np.float32)
