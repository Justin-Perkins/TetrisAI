import os
import sys

from pyboy import PyBoy, WindowEvent
from TetrisPyBoyGymEnv import CustomPyBoyGymEnv

quiet = "--quiet" in sys.argv
pyboy = PyBoy("Tetris.gb", game_wrapper=True)

assert pyboy.cartridge_title() == "TETRIS"

tetris = pyboy.game_wrapper()

gym = CustomPyBoyGymEnv(pyboy, observation_type="tiles", action_type="press")

# Get the number of possible actions
number_actions = gym.action_space.n

print(f"NUMBER OF ACTIONS: {number_actions}")

# Also resets/starts the game through the wrapper
observation = gym.reset()

pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
pyboy.tick()
pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)

number_iterations = 0

final_scores = []

while not pyboy.tick():
    for _ in range(10):
        pyboy.tick()

    action = gym.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, done, info = gym.step(action)

    print(action)

    if tetris.game_over():
        final_scores.append(tetris.score)

        observation = gym.reset()
    
    pass
