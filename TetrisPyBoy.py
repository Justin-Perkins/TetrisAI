import os

from TetrisPluginManager import CustomPluginManager
from pyboy import PyBoy

from pyboy.logging import get_logger

from pyboy.core.mb import Motherboard
from pyboy import botsupport

logger = get_logger(__name__)

SPF = 1 / 60. # inverse FPS (frame-per-second)

defaults = {
    "color_palette": (0xFFFFFF, 0x999999, 0x555555, 0x000000),
    "cgb_color_palette": ((0xFFFFFF, 0x7BFF31, 0x0063C5, 0x000000), (0xFFFFFF, 0xFF8484, 0x943A3A, 0x000000),
                          (0xFFFFFF, 0xFF8484, 0x943A3A, 0x000000)),
    "scale": 3,
    "window_type": "SDL2",
}

class CustomPyBoy(PyBoy):
    def __init__(
        self,
        gamerom_file,
        *,
        bootrom_file=None,
        disable_renderer=False,
        sound=False,
        sound_emulated=False,
        cgb=None,
        randomize=False,
        **kwargs
    ):
        
        self.initialized = False

        for k, v in defaults.items():
            if k not in kwargs:
                kwargs[k] = kwargs.get(k, defaults[k])

        if not os.path.isfile(gamerom_file):
            raise FileNotFoundError(f"ROM file {gamerom_file} was not found!")
        self.gamerom_file = gamerom_file

        self.mb = Motherboard(
            gamerom_file,
            bootrom_file or kwargs.get("bootrom"), # Our current way to provide cli arguments is broken
            kwargs["color_palette"],
            kwargs["cgb_color_palette"],
            disable_renderer,
            sound,
            sound_emulated,
            cgb,
            randomize=randomize,
        )

        self.plugin_manager = CustomPluginManager(self, self.mb, kwargs)

        super().__init__(
            gamerom_file,
            bootrom_file=bootrom_file,
            disable_renderer=disable_renderer,
            sound=sound,
            sound_emulated=sound_emulated,
            cgb=cgb,
            randomize=randomize,
            **kwargs
        )

    def game_wrapper(self):
        """
        Custom implementation of the game_wrapper function.
        """
        
        return self.plugin_manager.gamewrapper()
    
    def botsupport_manager(self):
        """

        Returns
        -------
        `pyboy.botsupport.BotSupportManager`:
            The manager, which gives easier access to the emulated game through the classes in `pyboy.botsupport`.
        """
        return botsupport.BotSupportManager(self, self.mb)
