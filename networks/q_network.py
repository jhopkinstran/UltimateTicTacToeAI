import torch.nn as nn
from abc import ABC, abstractmethod

class BaseNetwork(nn.Module, ABC):
    def __init__(self, input_shape, output_shape):
        super().__init__()
        self.input_shape = input_shape
        self.output_size = output_shape
    
    @abstractmethod
    def forward(self, x):
        pass

