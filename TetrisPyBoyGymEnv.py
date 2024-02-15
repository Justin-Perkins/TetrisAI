from pyboy.openai_gym import PyBoyGymEnv
from pyboy import WindowEvent

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
        
        # Redefine _buttons attribute with your desired subset
        self._buttons = [
            WindowEvent.PRESS_ARROW_DOWN, WindowEvent.PRESS_ARROW_RIGHT,
            WindowEvent.PRESS_ARROW_LEFT, WindowEvent.PRESS_BUTTON_A, WindowEvent.PRESS_BUTTON_B
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
