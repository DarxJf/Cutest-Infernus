from typing import Any
import pygame

from gale.state import BaseState

import settings
from src.States.Game.PlayState import PlayState


class SelectCharacterState(BaseState):
    def enter(
        self,
        characterIndex: int = 0,
    ) -> None:
        self.characterIndex = characterIndex
      
    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return
        
        charactersList = ["character1", "character2", "character2"]

        if inputId == "moveLeft":
            self.characterIndex = (self.characterIndex - 1) % len(charactersList)
            settings.SOUNDS["select"].play()
        elif inputId == "moveRight":
            self.characterIndex = (self.characterIndex + 1) % len(charactersList)
            settings.SOUNDS["select"].play()
        elif inputId == "enter":
            self._confirm()

    def _confirm(self) -> None:
        settings.SOUNDS["select"].play()
        self.state_machine.pop()
        self.state_machine.push(PlayState(self.state_machine))

    def render(self, surface: pygame.Surface) -> None:
        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]
        
        centerX = settings.VIRTUAL_WIDTH / 2
        centerY = settings.VIRTUAL_HEIGHT / 2

        titleText = medium.render("CHARACTER SELECT", True, (240, 220, 50))
        titleRect = titleText.get_rect(centerx=centerX, y=25)
        surface.blit(titleText, titleRect)

        panelRect = pygame.Rect(centerX - 50, centerY - 55, 100, 110)
        pygame.draw.rect(surface, (16, 16, 23), panelRect, border_radius=4) 
        pygame.draw.rect(surface, (200, 50, 100), panelRect, width=2, border_radius=4) 


        arrowRight = settings.FRAMES["cursors"][settings.TILE_IDS["arrowRight"]]
        arrowLeft = settings.FRAMES["cursors"][settings.TILE_IDS["arrowLeft"]]
        surface.blit(settings.TEXTURES["cursors"], (centerX - 70, centerY - 10), arrowLeft)
        surface.blit(settings.TEXTURES["cursors"], (centerX + 58, centerY - 10), arrowRight)

        startText = small.render("PRESS ENTER TO START GAME", True, (100, 100, 100))
        startRect = startText.get_rect(centerx=centerX, y=settings.VIRTUAL_HEIGHT - 45)
        surface.blit(startText, startRect)
