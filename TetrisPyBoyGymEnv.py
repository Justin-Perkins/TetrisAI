from pyboy.openai_gym import PyBoyGymEnv
from pyboy import WindowEvent

import numpy as np

try:
    from gym.spaces import Discrete
    enabled = True
except ImportError:

    class Env:
        pass

    enabled = False

class CustomPyBoyGymEnv(PyBoyGymEnv):
    def __init__(self, pyboy_instance, observation_type="tiles", action_type="press"):
        # Call the super constructor
        super().__init__(pyboy_instance, observation_type, action_type)
        
        # Building the action_space
        self._buttons = [
            WindowEvent.PRESS_ARROW_DOWN, WindowEvent.PRESS_ARROW_RIGHT,
            WindowEvent.PRESS_ARROW_LEFT, WindowEvent.PRESS_BUTTON_A, WindowEvent.PRESS_BUTTON_B
        ]

        self._buttons_release = [
            WindowEvent.RELEASE_ARROW_DOWN, WindowEvent.RELEASE_ARROW_RIGHT,
            WindowEvent.RELEASE_ARROW_LEFT, WindowEvent.RELEASE_BUTTON_A, WindowEvent.RELEASE_BUTTON_B
        ]
        
        # Update actions list and action_space
        self.actions = [self._DO_NOTHING] + self._buttons
        if action_type == "all":
            self.actions += self._buttons_release
        elif action_type not in ["press", "toggle"]:
            raise ValueError(f"action_type {action_type} is invalid")
        self.action_type = action_type

        # Update the action_space
        self.action_space = Discrete(len(self.actions))

    def calculate_density(self):
        highest_block = self.get_highest_block_below_piece()
        occupied_tiles = np.sum(self.game_wrapper.game_area()[:highest_block, :] != 47)
        total_tiles = highest_block * self.game_wrapper.shape[1]
        self.density = occupied_tiles / total_tiles

    def get_highest_block_below_piece(self):
        highest_block = 0
        for col in range(self.game_wrapper.shape[1]):
            for row in range(self.game_wrapper.shape[0] - 1, -1, -1):
                if self.game_wrapper.game_area()[row][col] != 47:  # If tile is occupied
                    highest_block = max(highest_block, row)
                    break  # Move to the next column once a non-blank tile is found
        return highest_block

    def step(self, action_id):
        info = {}

        action = self.actions[action_id]
        if action == self._DO_NOTHING:
            pyboy_done = self.pyboy.tick()
        else:
            if self.action_type == "toggle":
                if self._button_is_pressed[action]:
                    self._button_is_pressed[action] = False
                    action = self._release_button[action]
                else:
                    self._button_is_pressed[action] = True

            self.pyboy.send_input(action)
            pyboy_done = self.pyboy.tick()

            if self.action_type == "press":
                self.pyboy.send_input(self._release_button[action])

        highest_block = self.get_highest_block_below_piece()
        board_density = self.calculate_density()

        print(f"HIGHEST POINT: {highest_block}")
        print(f"GAME DENSITY: {board_density}")

        new_fitness = self.game_wrapper.fitness * (board_density + 0.2)
        reward = new_fitness - self.last_fitness
        self.last_fitness = new_fitness

        observation = self._get_observation()
        done = pyboy_done or self.game_wrapper.game_over()

        return observation, reward, done, False, info
    
    
