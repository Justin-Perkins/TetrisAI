from array import array

import numpy as np

import pyboy
from pyboy.utils import WindowEvent

from pyboy.plugins.game_wrapper_tetris import GameWrapperTetris

class CustomGameWrapperTetris(GameWrapperTetris):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.density = 0
        self.dead_tiles = 0

    def calculate_density(self):
        highest_block = self.get_highest_block_below_piece()
        occupied_tiles = np.sum(self._game_area_tiles()[:highest_block, :] != 47)
        total_tiles = highest_block * self.shape[1]
        self.density = occupied_tiles / total_tiles

    def get_highest_block_below_piece(self):
        highest_block = 0
        for col in range(self.shape[1]):
            for row in range(self.shape[0] - 1, -1, -1):
                if self._game_area_tiles()[row][col] != 47:  # If tile is occupied
                    highest_block = max(highest_block, row)
                    break  # Move to the next column once a non-blank tile is found
        return highest_block

    def calculate_dead_tiles(self):
        # Iterate through each tile
        self.dead_tiles = 0
        for i in range(1, self.shape[0] - 1):
            for j in range(1, self.shape[1] - 1):
                if self._game_area_tiles()[i][j] != 47:  # If tile is occupied
                    # Check if it's surrounded by other tiles or edges
                    if (self._game_area_tiles()[i - 1][j] != 47 and
                        self._game_area_tiles()[i + 1][j] != 47 and
                        self._game_area_tiles()[i][j - 1] != 47 and
                        self._game_area_tiles()[i][j + 1] != 47):
                        self.dead_tiles += 1

    def post_tick(self):
        super().post_tick()
        self.calculate_density()
        self.fitness = (self.score) * (self.density + 0.2)
