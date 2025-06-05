from replay_buffer import ReplayBuffer
from networks.q_network import BaseNetwork
from agent import Agent
from typing import Tuple
from game_state import GameState
import copy
import torch
from encoders.flat_encoder import FlatEncoder
import random
import numpy as np

class DQAgent(Agent):
    def __init__(self, 
                 network: BaseNetwork, 
                 state_dim: int, 
                 action_dim: int, 
                 replay_buffer_size: int=10000, 
                 batch_size:int=64, 
                 lr: float = 1e-3, 
                 gamma: float = 0.99, 
                 epsilon_start: float = 1.0, 
                 epsilon_final: float = 0.01, 
                 epsilon_decay: int = 5000,
                 steps_reset: int = 1000,
                 device: str = "cpu"):
        
        super().__init__()
        
        # Q-Network Information
        self.network = network.to(device)
        self.target_network = copy.deepcopy(network).to(device)
        self.target_network.eval()
        self.optimizer = torch.optim.Adam(self.network.parameters(), lr=lr)
        
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        self.replay_buffer = ReplayBuffer(replay_buffer_size, device)

        self.batch_size = batch_size

        # Hyperparameters for Reinforcement Learning
        self.lr = lr
        self.gamma = gamma

        self.epsilon_start = epsilon_start
        self.epsilon_final = epsilon_final
        self.epsilon_decay = epsilon_decay
        self.steps = 0

        self.device = device

    def get_action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        valid_actions = game_state.get_valid_actions()
        if not valid_actions:
            raise ValueError("No valid actions available to DQN Agent")

        encoder = FlatEncoder()
        encoding = encoder.encode(game_state)
        state_tensor = torch.tensor(encoding, dtype=torch.float32, device = self.device)

        with torch.no_grad():
            q_values = self.network(state_tensor)[0].cpu().numpy()

        epsilon = self.compute_epsilon().item()
        self.steps += 1

        if random.random() < epsilon:
            return random.choice(valid_actions)
        
        masked_q_values = np.full_like(q_values, -np.inf)
        for action in valid_actions:
            idx = self.action_to_index(action)
            masked_q_values[idx] = q_values[idx]

        best_idx = np.argmax(masked_q_values)
        return self.index_to_action(best_idx)

    def compute_epsilon(self):
        return self.epsilon_final + (self.epsilon_start - self.epsilon_final) * \
               torch.exp(-torch.tensor(self.steps / self.epsilon_decay))

    def action_to_index(self, action: Tuple[int, int, int, int]) -> int:
        ult_r, ult_c, r, c = action
        return (ult_r * 3 + ult_c) * 9 + (r * 3 + c)

    def index_to_action(self, index: int) -> Tuple[int, int, int, int]:
        board_idx = index // 9
        cell_idx = index % 9
        return (board_idx // 3, board_idx % 3, cell_idx // 3, cell_idx % 3)

    def train_step(self):
        if len(self.replay_buffer) < self.batch_size:
            return
        
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)

        q_values = self.network(states)
        action_indices = actions.unsqueeze(1)
        current_q = q_values.gather(1, action_indices).squeeze(1)

        with torch.no_grad():
            next_q_values = self.target_network(next_states)
            max_next_q = next_q_values.max(dim=1)[0]
            target_q = rewards + (1 - dones) * self.gamma * max_next_q

        loss = torch.nn.functional.mse_loss(current_q, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
    
    def update_target_network(self):
        self.target_network.load_state_dict(self.network.state_dict())