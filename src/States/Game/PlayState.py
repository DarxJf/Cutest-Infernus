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
        self.testEnemy = BattleEntity(x = 5, y = 5, definition=ENEMIES.get("skeleton"))

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

            
    def render(self, surface: pygame.Surface) -> None:
        self.room.render(surface)

        offsetX = self.room.offsetX
        offsetY = self.room.offsetY

        # Entities
        for entity in self.entities:
            entity.render(surface, offsetX, offsetY)

        for enemy in self.enemies:
            enemy.render(surface, offsetX, offsetY)
