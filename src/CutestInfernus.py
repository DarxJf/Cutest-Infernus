"""

"""

import pygame

from gale.game import Game
from gale.input_handler import InputData
from gale.state import StateStack

import settings
from src.States.Game.StartState import StartState

# Name probably will change
class CutestInfernus(Game):
    def init(self) -> None:
        self.stateStack = StateStack()
        self.stateStack.push(StartState(self.stateStack))

    def update(self, dt: float) -> None:
        self.stateStack.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.stateStack.render(surface)

    def on_input(self, inputId: str, inputData: InputData) -> None:
        if inputId == "quit" and inputData.pressed:
            self.quit()
        else:
            self.stateStack.on_input(inputId, inputData)