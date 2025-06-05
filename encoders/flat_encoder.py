# Encoder stores the 81 squares, 9 win states, and player turn
from base_encoder import StateEncoder
import numpy as np
from game_state import GameState
class FlatEncoder(StateEncoder):
    def encode(self, game_state: GameState):
        """
        Returns an encoding of the game state.

        The encoding format:
        - First 81 numbers represent the squares (flattened 9x9 board),
        - Next 9 represent the winner of each miniboard,
        - Last number represents the current player's turn.

        Total length: 90.

        Args:
            game_state (GameState): The current gamestate of the board.

        Returns:
            np.ndarray: A length-90 array of dtype np.float32 representing the game state.
        """
        board = game_state.board
        flat_grid = []
        mini_results = []

        for ult_r in range(3):
            for ult_c in range(3):
                mini = board.get_mini_board(ult_r, ult_c)
                for r in range(3):
                    for c in range(3):
                        flat_grid.append(mini.grid[r][c])
                mini_results.append(mini.winner if mini.winner else 0)

        flat_grid += mini_results
        flat_grid.append(game_state.player_turn)
        return np.array(flat_grid, dtype=np.float32)
