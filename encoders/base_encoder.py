from abc import ABC, abstractmethod

class StateEncoder(ABC):
    @abstractmethod
    def encode(self, game_state):
        """
        Encode the given game state into a numeric array representation.

        Args:
            game_state: The current state of the game to encode.

        Returns:
            np.ndarray: Encoded numeric representation of the game state.
        """
        pass