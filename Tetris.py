import sys

from pathlib import Path
import datetime

from pyboy import PyBoy
from TetrisPyBoyGymEnv import CustomPyBoyGymEnv

import torch

from Logging import MetricLogger
from Agent import Agent
from testing.dqn_agent import DQNAgent

quiet = "--quiet" in sys.argv
pyboy = PyBoy("Tetris.gb", game_wrapper=True)

assert pyboy.cartridge_title() == "TETRIS"

tetris = pyboy.game_wrapper()

gym = CustomPyBoyGymEnv(pyboy, observation_type="tiles", action_type="all")

use_cuda = torch.cuda.is_available()
print(f"Using CUDA: {use_cuda}")
print()

save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
save_dir.mkdir(parents=True)

episodes = 2000
max_steps = None
epsilon_stop_episode = 1500
mem_size = 20000
discount = 0.95
batch_size = 512
epochs = 1
render_every = 50
log_every = 50
replay_start_size = 2000
train_every = 1
n_neurons = [32, 32]
render_delay = None
activations = ['relu', 'relu', 'linear']
agent = DQNAgent(4,
                     n_neurons=n_neurons, activations=activations,
                     epsilon_stop_episode=epsilon_stop_episode, mem_size=mem_size,
                     discount=discount, replay_start_size=replay_start_size)

logger = MetricLogger(save_dir)

# Also resets/starts the game through the wrapper
observation = gym.reset()

# Get the number of possible actions
number_actions = gym.action_space.n

# Confirm reduced number of actions
print(f"NUMBER OF ACTIONS: {number_actions}")

pyboy.set_emulation_speed(0)

episodes = 400000
for e in range(episodes):
    print(f"EPISODE: {e}")

    state = gym.reset()

    # Play the game!
    while True:

        # Run agent on the state
        action = agent.act(state)

        # Agent performs action
        next_state, reward, done, trunc, info = gym.step(action)

        # Remember
        agent.cache(state, next_state, action, reward, done)

        # Learn
        q, loss = agent.learn()

        # Logging
        logger.log_step(reward, loss, q)

        # Update state
        state = next_state

        # Check if end of game
        if tetris.game_over():
            break

    logger.log_episode()

    if (e % 40 == 0) or (e == episodes - 1):
        logger.record(episode=e, epsilon=agent.exploration_rate, step=agent.curr_step)