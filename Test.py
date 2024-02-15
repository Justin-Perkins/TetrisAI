import sys

from pyboy import PyBoy, WindowEvent

quiet = "--quiet" in sys.argv
pyboy = PyBoy("Tetris.gb", game_wrapper=True)

assert pyboy.cartridge_title() == "TETRIS"

tetris = pyboy.game_wrapper()

pyboy.set_emulation_speed(1)

# Also resets/starts the game through the wrapper
tetris.start_game()

pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
pyboy.tick()
pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)


while not pyboy.tick():

    if tetris.game_over():
        tetris.reset_game()
    pass
