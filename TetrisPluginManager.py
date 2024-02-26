from pyboy.plugins.manager import PluginManager
from TetrisGameWrapper import CustomGameWrapperTetris

class CustomPluginManager(PluginManager):
    def __init__(self, pyboy, mb, pyboy_argv):
        super().__init__(pyboy, mb, pyboy_argv)
        self.game_wrapper_tetris = CustomGameWrapperTetris(pyboy, mb, pyboy_argv)