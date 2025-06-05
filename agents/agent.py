from abc import ABC, abstractmethod
from game_state import GameState
from typing import Tuple

class Agent(ABC):

    @abstractmethod
    def get_action(self, game_state:GameState) -> Tuple[int, int, int, int]:
        """
        Returns an action given a game state.

        Args:
            game_state (GameState): The current state of the game.
        
        Returns:
            Tuple[int, int, int, int]: The move to be played by the agent in the form 
            of (ult_row, ult_col, row, col).
        """
        pass