
import sys
from pathlib import Path
from pyboy import PyBoy
import torch
from dqn_agent import DQNAgent
import numpy as np

from tetris import Tetris

from tqdm import tqdm
from datetime import datetime

from statistics import mean, median
from logs import CustomTensorBoard
        
def dqn():
    env = Tetris()
    episodes = 3000
    max_steps = None
    epsilon_stop_episode = 2000
    mem_size = 10000
    discount = 0.95
    batch_size = 128
    epochs = 1
    render_every = 50
    log_every = 50
    replay_start_size = 2000
    train_every = 1
    n_neurons = [32, 32]
    render_delay = None
    activations = ['relu', 'relu', 'linear']

    agent = DQNAgent(env.get_state_size(),
                     n_neurons=n_neurons, activations=activations,
                     epsilon_stop_episode=epsilon_stop_episode, mem_size=mem_size,
                     discount=discount, replay_start_size=replay_start_size)
    
    #agent.load('my_model.keras')
    
    log_dir = f'logs/tetris-nn={str(n_neurons)}-mem={mem_size}-bs={batch_size}-e={epochs}-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
    log = CustomTensorBoard(log_dir=log_dir)

    scores = []

    for episode in tqdm(range(episodes)):
        current_state = env.reset()
        done = False
        steps = 0

        render = True

        # Game
        while not done and (not max_steps or steps < max_steps):
            next_states = env.get_next_states()
            best_state = agent.best_state(next_states.values())
            
            best_action = None
            for action, state in next_states.items():
                if state == best_state:
                    best_action = action
                    break

            reward, done = env.play(best_action[0], best_action[1], render=render,
                                    render_delay=render_delay)
            
            agent.add_to_memory(current_state, next_states[best_action], reward, done)
            current_state = next_states[best_action]
            steps += 1

        scores.append(env.get_game_score())

        # Train
        if episode % train_every == 0:
            agent.train(batch_size=batch_size, epochs=epochs)

        # Logs
        if episode % 40 == 0:
            print("Saving checkpoint")
            avg_score = mean(scores[-log_every:])
            min_score = min(scores[-log_every:])
            max_score = max(scores[-log_every:])

            log.log(episode, avg_score=avg_score, min_score=min_score,
                    max_score=max_score)
            checkpoint_dir = Path("training_checkpoints5")
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            save_dir = checkpoint_dir / (datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".weights.h5")
            agent.checkpoint(save_dir)

    agent.save("my_model4.keras")


if __name__ == "__main__":
    dqn()
    