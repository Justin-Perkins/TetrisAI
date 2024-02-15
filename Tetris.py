import os
import sys

import datetime

from pyboy import PyBoy, WindowEvent
from TetrisPyBoyGymEnv import CustomPyBoyGymEnv

import torch
import torch.nn as nn
from torch.distributions.normal import Normal

quiet = "--quiet" in sys.argv
pyboy = PyBoy("Tetris.gb", game_wrapper=True)

assert pyboy.cartridge_title() == "TETRIS"

tetris = pyboy.game_wrapper()

gym = CustomPyBoyGymEnv(pyboy, observation_type="tiles", action_type="press")

# Also resets/starts the game through the wrapper
observation = gym.reset()

# Get the number of possible actions
number_actions = gym.action_space.n

# Confirm reduced number of actions
print(f"NUMBER OF ACTIONS: {number_actions}")

pyboy.set_emulation_speed(1)

pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
pyboy.tick()
pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)

number_iterations = 0

now = datetime.datetime.now()

scores = open("Scores.txt", "a")
scores.write(f"\nSCORES FOR {now}:")
scores.close()


while not pyboy.tick():
    for _ in range(10):
        pyboy.tick()

    action = gym.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, done, info = gym.step(action)

    if tetris.game_over():
        
        print(tetris.score)

        scores = open("Scores.txt", "a")
        scores.write(f"\n{tetris.score}")
        scores.close()

        observation = gym.reset()
    
    pass
