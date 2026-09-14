from typing import Any, Dict, Optional
import pygame

from gale.state import BaseState

import settings
from src.States.Game.PauseMenuState import PauseMenuState

from src.States.Game.BatleState import BattleState
from src.States.Game.SelectTargetState import SelectTargetState
from src.Definitions.Entity import PLAYER_CHARACTERS, ENEMIES
from src.Models.Room import Room
from src.Models.BattleEntity import BattleEntity


class PlayState(BaseState):
    def enter(self, **kwargs: dict) -> None:
        # glow
        self.glowSurface = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(
            self.glowSurface, 
            (0, 150, 255, 128), 
            (0, 0, settings.TILE_SIZE, settings.TILE_SIZE)
        )

        # Room
        self.room = Room(cols=20, rows=12)

        # character and entities
        self.charKey = kwargs.get("character_selected", 0)

        charNames = { # Could change this in SelectCharacterState
            0: "Cloud",
            1: "Chloe",
            2: "Balthazar",
            3: "Pelusa",
        }
        characterName = charNames.get(self.charKey, "Cloud")
        self.definition = PLAYER_CHARACTERS.get(characterName)

        spawnX, spawnY = 3, 3

        self.playerChar = BattleEntity(x = spawnX, y = spawnY, definition = self.definition)
        self.testEnemy = BattleEntity(x = 10, y = 10, definition=ENEMIES.get("slime"))

        self.entities: list[BattleEntity] = [self.playerChar]
        self.enemies = [self.testEnemy]

    def update(self, dt: float) -> None:
        self.room.update(dt)

    def exit(self) -> None:
        # for char in self.party.characters.Values():
        #     char.clear_status()
        pass

    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return
        elif inputId == "pause":
            self.state_machine.push(PauseMenuState(self.state_machine))

        elif inputId == "enter":
            # self.room = Room(cols=20, rows=12)
            self.state_machine.push(BattleState(self.state_machine), self.entities, self.enemies, room = self.room)

        elif inputId == "space":
            reachable = self.playerChar.get_reachable_tiles(self.room.is_walkable)
 
            self.reachableTiles = reachable 

            def on_test_target_selected(targetX: int, targetY: int) -> None:
                self.playerChar.mapX = targetX
                self.playerChar.mapY = targetY

                print(f"Posiciones logicas nuevas: {self.playerChar.mapX} , {self.playerChar.mapY}")

                self.playerChar.x = targetX * settings.TILE_SIZE
                self.playerChar.y = targetY * settings.TILE_SIZE

                self.reachableTiles = set()

            self.state_machine.push(
                SelectTargetState(self.state_machine),
                actor=self.playerChar,
                action=None,
                enemies=self.enemies,
                callback=on_test_target_selected,
                boardCols=self.room.cols,
                boardRows=self.room.rows,
                validTiles=reachable,  # Pasamos la restricción matemática
                offsetX=self.room.offsetX,
                offsetY=self.room.offsetY
            )
            
    def render(self, surface: pygame.Surface) -> None:
        self.room.render(surface)

        offsetX = self.room.offsetX
        offsetY = self.room.offsetY
        
        # render Glow
        if hasattr(self, 'reachableTiles') and self.reachableTiles:
            for gridX, gridY in self.reachableTiles:
                self._glow_tile(surface, gridX, gridY, offsetX, offsetY)

        # Entities
        for entity in self.entities:
            entity.render(surface, offsetX, offsetY)

        for enemy in self.enemies:
            enemy.render(surface, offsetX, offsetY)

    def _glow_tile(self, surface: pygame.Surface, gridX: int, gridY: int, offsetX, offsetY) -> None:
        pixelX = gridX * settings.TILE_SIZE + offsetX
        pixelY = gridY * settings.TILE_SIZE + offsetY

        surface.blit(self.glowSurface, (pixelX, pixelY))
        
    