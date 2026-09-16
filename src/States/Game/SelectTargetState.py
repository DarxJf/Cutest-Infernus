from typing import Any, Callable
import pygame

from gale.state import BaseState

import settings
from src.Utils.AoeCalculator import AoECalculator


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
        glowSurface: pygame.Surface = None,
    ) -> None:
        self.actor = actor
        self.action = action
        self.callback = callback
        self.boardCols = boardCols
        self.boardRows = boardRows

        self.validTiles = validTiles
        self.glowSurface = glowSurface

        self.offsetX = offsetX
        self.offsetY = offsetY
        
        self.cursorX = actor.mapX
        self.cursorY = actor.mapY

        if action and action.areaType == "single" and enemies and self.validTiles:
            valid_enemies = [
                e for e in enemies 
                if not getattr(e, 'dead', False) and (e.mapX, e.mapY) in self.validTiles
            ]
            
            if valid_enemies:
                nearest = min(
                    valid_enemies,
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

            if self.validTiles and (self.cursorX, self.cursorY) not in self.validTiles:
                return

            self.state_machine.pop()
            self.callback(self.cursorX, self.cursorY)
            
        elif inputId == "escape":
            self.state_machine.pop()

    def render(self, surface: pygame.Surface) -> None:
        if self.action and self.action.areaType in ["cross", "square"] and self.glowSurface:
            affected = set()

            if self.action.areaType == "cross":
                affected = AoECalculator.get_linear_cross(
                    self.actor.mapX, self.actor.mapY, self.action.gridRange, self.boardCols, self.boardRows
                )
            elif self.action.areaType == "square":
                affected = AoECalculator.get_square_area(
                    self.actor.mapX, self.actor.mapY, self.action.areaRadius, self.boardCols, self.boardRows
                )

            for gx, gy in affected:
                px = gx * settings.TILE_SIZE + self.offsetX
                py = gy * settings.TILE_SIZE + self.offsetY
                surface.blit(self.glowSurface, (px, py))

        pixelX = self.cursorX * settings.TILE_SIZE + self.offsetX
        pixelY = self.cursorY * settings.TILE_SIZE + self.offsetY

        pygame.draw.rect(
            surface, 
            (255, 255, 0),
            (pixelX, pixelY, settings.TILE_SIZE, settings.TILE_SIZE), 
            2
        )