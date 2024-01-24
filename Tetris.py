import os
import sys

from pyboy import PyBoy, WindowEvent
from pyboy.openai_gym import PyBoyGymEnv

quiet = "--quiet" in sys.argv
pyboy = PyBoy("Tetris.gb", game_wrapper=True)

assert pyboy.cartridge_title() == "TETRIS"

tetris = pyboy.game_wrapper()
gym = PyBoyGymEnv(pyboy, observation_type="tiles", action_type="press")

tetris.start_game()

pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
pyboy.tick()
pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)

while not pyboy.tick():
    pass
