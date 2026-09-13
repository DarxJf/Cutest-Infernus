from typing import Any, Dict, Optional
import pygame

from gale.state import BaseState

import settings
from src.States.Game.PauseMenuState import PauseMenuState

from src.Models.Room import Room


class PlayState(BaseState):
    def enter(self) -> None:
        # glow
        self.glowSurface = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(
            self.glowSurface, 
            (0, 150, 255, 128), 
            (0, 0, settings.TILE_SIZE, settings.TILE_SIZE)
        )
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

        if hasattr(self, 'reachableTiles') and self.reachableTiles:
            for gridX, gridY in self.reachableTiles:
                self._glow_tile(surface, gridX, gridY)

    def _glow_tile(self, surface: pygame.Surface, gridX: int, gridY: int) -> None:
        pixelX = gridX * settings.TILE_SIZE
        pixelY = gridY * settings.TILE_SIZE

        surface.blit(self.glowSurface, (pixelX, pixelY))
        
    