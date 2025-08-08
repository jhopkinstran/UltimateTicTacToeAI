from game_env import UltimateTicTacToeEnv
from encoders import FlatEncoder
from game_env import compute_reward
import random

def train(agent, encoder, num_episodes=1000, max_steps_per_episode=100, prefill_size=1000):
    env = UltimateTicTacToeEnv(ruleset="default")

    print("Prefilling replay buffer with random actions...")
    while len(agent.replay_buffer) < prefill_size:
        env.reset()
        done = False
        steps = 0
        while not done and steps < max_steps_per_episode:
            valid_actions = env.get_valid_actions()
            if not valid_actions:
                break
            action = random.choice(valid_actions)
            prev_encoded = encoder.encode(env)

            env.make_move(*action)
            next_encoded = encoder.encode(env)
            reward = compute_reward(env, agent_player=env.player_turn * -1)
            done = env.game_over

            agent.replay_buffer.push(prev_encoded, agent.action_to_index(action), reward, next_encoded, done)
            steps += 1

    print("Starting self-play training...")
    for episode in range(num_episodes):
        env.reset()
        done = False
        total_reward = 0
        steps = 0

        while not done and steps < max_steps_per_episode:
            state_encoded = encoder.encode(env)
            action = agent.get_action(env)
            prev_encoded = state_encoded

            env.make_move(*action)
            next_encoded = encoder.encode(env)
            done = env.game_over
            reward = compute_reward(env, agent_player=env.player_turn * -1)  # last player who moved

            agent.replay_buffer.push(prev_encoded, agent.action_to_index(action), reward, next_encoded, done)
            loss = agent.train_step()

            total_reward += reward
            steps += 1

        print(f"Episode {episode+1}, Total Reward: {total_reward}, Replay Buffer Size: {len(agent.replay_buffer)}")
