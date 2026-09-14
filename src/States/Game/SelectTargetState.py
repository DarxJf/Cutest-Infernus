from typing import Any, Callable
import pygame

from gale.state import BaseState

import settings


class SelectTargetState(BaseState):
    def enter(
        self, 
        actor: Any, 
        action: Any, 
        enemies: list, 
        callback: Callable[[int, int], None], 
        boardCols: int = 20, 
        boardRows: int = 12,
        validTiles: set = None,
        offsetX: int = 0,
        offsetY: int = 0,
    ) -> None:
        self.actor = actor
        self.action = action
        self.callback = callback
        self.boardCols = boardCols
        self.boardRows = boardRows

        self.validTiles = validTiles

        self.offsetX = offsetX
        self.offsetY = offsetY
        
        self.cursorX = actor.mapX
        self.cursorY = actor.mapY

        if action and action.areaType == "single" and enemies:
            alive_enemies = [e for e in enemies if not getattr(e, 'dead', False)]
            if alive_enemies:
                nearest = min(
                    alive_enemies,
                    key=lambda e: abs(e.mapX - actor.mapX) + abs(e.mapY - actor.mapY)
                )
                self.cursorX = nearest.mapX
                self.cursorY = nearest.mapY

    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return

        if inputId == "moveLeft" and self.cursorX > 0:
            self.cursorX -= 1
        elif inputId == "moveRight" and self.cursorX < self.boardCols - 1:
            self.cursorX += 1
        elif inputId == "moveUp" and self.cursorY > 0:
            self.cursorY -= 1
        elif inputId == "moveDown" and self.cursorY < self.boardRows - 1:
            self.cursorY += 1
            
        elif inputId == "enter":
            if self.action is None:
                if (self.cursorX, self.cursorY) in self.validTiles:
                    self.state_machine.pop()
                    self.callback(self.cursorX, self.cursorY)
                else:
                    print("Invalid Tile")
            else:
                self.state_machine.pop()
                self.callback(self.cursorX, self.cursorY)
            
        elif inputId == "escape":
            self.state_machine.pop()

    def render(self, surface: pygame.Surface) -> None:
        pixelX = self.cursorX * settings.TILE_SIZE + self.offsetX
        pixelY = self.cursorY * settings.TILE_SIZE + self.offsetY

        pygame.draw.rect(
            surface, 
            (255, 255, 0), # Color amarillo
            (pixelX, pixelY, settings.TILE_SIZE, settings.TILE_SIZE), 
            2 # Grosor de la línea
        )