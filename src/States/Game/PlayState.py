from typing import Any, Dict, Optional
import pygame

from gale.state import BaseState

import settings
from src.States.Game.PauseMenuState import PauseMenuState
from src.States.Game.RunState import RunState
from src.States.Game.DialogueState import DialogueState
from src.Definitions.Entity import PLAYER_CHARACTERS
from src.Models.Room import Room
from src.Models.BattleEntity import BattleEntity
from src.States.Game.RunState import RunState
from src.Utils.SpawnHelper import find_free_tile
from src.Utils.EncounterGenerator import generate_horde, generate_boss_encounter
from src.States.Game.DialogueState import DialogueState
from src.Definitions.Texts import INTRO_TEXT, PLAY_TUTORIAL_TEXT

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

        self.partySpawnAnchor = (3, self.room.rows - 3)
        occupied = set()

        leader = self.runState.party.lead()
        if leader is None:
            leader = BattleEntity(x=0, y= 0, definition=PLAYER_CHARACTERS["Cloud"]),
            leader.key = "Cloud"

        tile = find_free_tile(
            self.room,
            self.partySpawnAnchor[0],
            self.partySpawnAnchor[1],
            occupied,
        )
        if tile is None:
            tile(3, 3)

        leader.mapX, leader.mapY = tile
        leader.x = tile [0] * settings.TILE_SIZE
        leader.y = tile [1] * settings.TILE_SIZE
        occupied.add(tile)

        self.playerChar = leader

        def show_play_tutorial():
            if not self.runState.seenPlayTutorial:
                self.runState.seenPlayTutorial = True
                self.state_machine.push(
                    DialogueState(self.state_machine),
                    text=PLAY_TUTORIAL_TEXT,
                    position="top",
                )

        if not self.runState.seenIntro:
            self.runState.seenIntro = True
            self.state_machine.push(
                DialogueState(self.state_machine),
                text=INTRO_TEXT,
                position="bottom",
                onClose=show_play_tutorial,    
            )

    def update(self, dt: float) -> None:
        self.room.update(dt)
        self.playerChar.update(dt)
   

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

    def _start_battle(self) -> None:
        from src.States.Game.BatleState import BattleState

        if self.runState.shouldSpawnBoss():
            horde = generate_boss_encounter(
                self.runState.battlesFought,
                self.runState.bossesDefeated,
                )
            isBoss = True
        else:
            horde = generate_horde(self.runState.battlesFought)
            isBoss = False

        enemies = [
            BattleEntity(x = 0, y = 0, definition=defn)
            for defn in horde
        ]

        self.state_machine.push(
            BattleState(self.state_machine),
            runState=self.runState,
            enemies=enemies,
            room=self.room,
            isBoss =isBoss
        )

    def render(self, surface: pygame.Surface) -> None:
        self.room.render(surface)

        offsetX = self.room.offsetX
        offsetY = self.room.offsetY

        self.playerChar.render(surface, offsetX, offsetY)
        
