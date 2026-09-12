from typing import Any, Dict, Optional
import pygame

from gale.state import BaseState

import settings
from src.States.Game.PauseMenuState import PauseMenuState


class PlayState(BaseState):
    def enter(self) -> None:
        # glow
        self.glowSurface = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(
            self.glowSurface, 
            (0, 150, 255, 128), 
            (0, 0, settings.TILE_SIZE, settings.TILE_SIZE)
        )

    def update(self, dt: float) -> None:
        pass

    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return
        elif inputId == "pause":
            self.state_machine.push(PauseMenuState(self.state_machine))
     
    def render(self, surface: pygame.Surface) -> None:

        if hasattr(self, 'reachableTiles') and self.reachableTiles:
            for gridX, gridY in self.reachableTiles:
                self._glow_tile(surface, gridX, gridY)
     
        large = settings.FONTS["large"]
        medium = settings.FONTS["medium"]

        title = large.render("Run in progress", True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(settings.VIRTUAL_WIDTH / 2, 40)))


        hint = medium.render("P: pause menu ", True, (150, 150, 150))
        surface.blit(hint, hint.get_rect(center=(settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT - 20)))

    def _glow_tile(self, surface: pygame.Surface, gridX: int, gridY: int) -> None:
        pixelX = gridX * settings.TILE_SIZE
        pixelY = gridY * settings.TILE_SIZE

        surface.blit(self.glowSurface, (pixelX, pixelY))
    