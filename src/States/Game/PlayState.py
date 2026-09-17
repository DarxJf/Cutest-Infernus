from typing import Any, Dict, Optional
import pygame

from gale.state import BaseState

import settings
from src.States.Game.PauseMenuState import PauseMenuState

from src.States.Game.BatleState import BattleState
from src.States.Game.RestState import RestState
from src.States.Game.RunState import RunState
from src.Definitions.Entity import PLAYER_CHARACTERS, ENEMIES
from src.Models.Room import Room
from src.Models.BattleEntity import BattleEntity
from src.States.Game.RunState import RunState


class PlayState(BaseState):
    def enter(self, **kwargs: dict) -> None:
        # Room
        self.room = Room(cols=20, rows=12)

        #RunState
        incomingRunState: Optional[RunState] = kwargs.get("run_state")
        incomingDict: Optional[Dict[str, Any]] = kwargs.get("run_state_dict")

        if incomingRunState is not None:
            self.runState = incomingRunState

        elif incomingDict is not None:
            leaderKey = incomingDict["party"]["members"][0]["key"]
            self.runState = RunState(leaderKey=leaderKey, startingSouls=0)
            self.runState.load_dict(incomingDict)
        else:
            leaderKey: str = kwargs.get("character_selected", "Cloud")
            self.runState = RunState(leaderKey=leaderKey, startingSouls=200)

        self.playerChar = self.runState.party.lead()
        if self.playerChar is None:
            self.playerChar = BattleEntity(
                x=3, y=3, definition=PLAYER_CHARACTERS["Cloud"],
            )
            self.playerChar.key = "Cloud"        

        self.playerChar.mapX = 3
        self.playerChar.mapY = 3
        self.playerChar.x = 3 * settings.TILE_SIZE
        self.playerChar.y = 3 * settings.TILE_SIZE

        self.testEnemy = BattleEntity(x = 5, y = 5, definition=ENEMIES.get("slime"))

    def update(self, dt: float) -> None:
        self.room.update(dt)
        self.playerChar.update(dt)
        self.testEnemy.update(dt)

    def exit(self) -> None:
        for char in self.party.characters.Values():
            char.clear_status()
   
    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return
        elif inputId == "pause":
            self.state_machine.push(
                PauseMenuState(self.state_machine),
                runState = self.runState,
                )

        elif inputId == "enter":
            self._start_battle()
            return

        elif inputId == "space":
            self._open_rest_area()

    def _start_battle(self) -> None:
        """Push BattleState with the current RunState."""
        from src.States.Game.BatleState import BattleState

        # For now, always fight the same test enemy.
        # Later: replace with a region-driven encounter.
        enemies = [
            BattleEntity(x=10, y=5, definition=ENEMIES["slime"]),
            BattleEntity(x=12, y=7, definition=ENEMIES["slime"]),
        ]

        self.state_machine.push(
            BattleState(self.state_machine),
            runState=self.runState,
            enemies=enemies,
            room=self.room,
        )

    def _open_rest_area(self) -> None:
    # for debug
        self.state_machine.push(
            RestState(self.state_machine),
            runState=self.runState,
        )
        
    def render(self, surface: pygame.Surface) -> None:
        self.room.render(surface)

        offsetX = self.room.offsetX
        offsetY = self.room.offsetY

        for member in self.runState.party.members:
            member.render(surface, offsetX, offsetY)
