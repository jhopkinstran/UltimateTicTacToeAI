from abc import ABC, abstractmethod

class StateEncoder(ABC):
    @abstractmethod
    def encode(self, game_state):
        pass