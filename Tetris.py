import os
import sys

from pyboy import PyBoy, WindowEvent

quiet = "--quiet" in sys.argv
pyboy = PyBoy("Tetris.gb", game_wrapper=True)

assert pyboy.cartridge_title() == "TETRIS"

tetris = pyboy.game_wrapper()
tetris.start_game()

print(tetris)

pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
pyboy.tick()
pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)

while not pyboy.tick():
    pass