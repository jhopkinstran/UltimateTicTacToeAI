import torch
import torch.nn as nn
from q_network import BaseNetwork

class MLPNetwork(BaseNetwork):
    def __init__(self, input_shape, output_shape, hidden_dims=[128, 128], activation=nn.ReLU):
        super().__init__()
        layers = []
        last_dim = input_shape
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(last_dim, hidden_dim))
            layers.append(activation())
            last_dim = hidden_dim
        layers.append(nn.Linear(last_dim, output_shape))
        
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)
