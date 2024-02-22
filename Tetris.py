import sys

from pathlib import Path
import datetime

from pyboy import PyBoy, WindowEvent
from TetrisPyBoyGymEnv import CustomPyBoyGymEnv

import torch

from Logging import MetricLogger
from Agent import Agent

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

agent = Agent(state_dim=(1, 32, 32), action_dim=gym.action_space.n, save_dir=save_dir)

logger = MetricLogger(save_dir)

# Also resets/starts the game through the wrapper
observation = gym.reset()

# Get the number of possible actions
number_actions = gym.action_space.n

# Confirm reduced number of actions
print(f"NUMBER OF ACTIONS: {number_actions}")

pyboy.set_emulation_speed(1)

episodes = 40
for e in range(episodes):

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
        if done:
            break

    logger.log_episode()

    if (e % 20 == 0) or (e == episodes - 1):
        logger.record(episode=e, epsilon=agent.exploration_rate, step=agent.curr_step)