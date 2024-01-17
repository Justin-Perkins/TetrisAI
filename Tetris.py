from pyboy import PyBoy
from pyboy import WindowEvent

pyboy = PyBoy('Tetris.gb')

for i in range(150):
    pyboy.tick()

pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
pyboy.tick()
pyboy.tick()
pyboy.tick()
pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
pyboy.tick()
pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
pyboy.tick() # Process one frame to let the game register the input
pyboy.tick()
pyboy.tick()
pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)

print("End of Instructions")

pil_image = pyboy.screen_image()
pil_image.save('screenshot.png')

while not pyboy.tick():
    pass
pyboy.stop()