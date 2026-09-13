from typing import Any, Dict, Optional
import pygame

from gale.state import BaseState

import settings
from src.States.Game.PauseMenuState import PauseMenuState

from src.Models.Room import Room


class PlayState(BaseState):
    def enter(self) -> None:
        self.room = Room(cols=20, rows=12)

    def update(self, dt: float) -> None:
         self.room.update(dt) 

    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return
        elif inputId == "pause":
            self.state_machine.push(PauseMenuState(self.state_machine))

        elif inputId == "enter":
            self.room = Room(cols=20, rows=12)
     
    def render(self, surface: pygame.Surface) -> None:
        self.room.render(surface)
    