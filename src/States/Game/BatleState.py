from typing import List, Optional, Any
import pygame
from gale.state import BaseState

import settings
from src.Utils.TurnQueue import TurnQueue
from src.Models.BattleEntity import BattleEntity
from src.Gui.BatleUI import BattleUI
from src.Gui.BatleResultUI import BattleResultUI


class BattleState(BaseState):
    def enter(
        self,
        partyUnits: List[BattleEntity],
        enemyUnits: List[BattleEntity],
    ) -> None:
        self.party = partyUnits
        self.enemies = enemyUnits

        allUnits = self.party + self.enemies
        self.turnQueue = TurnQueue(allUnits)

        self.ui = BattleUI()
        
        self.currentActor = None
        self.upcomingTurns = []

        self.earnedSouls = 0
        self.battleOver = False      
        self.resultUI = None 
        
        self.start_next_turn()

    def start_next_turn(self) -> None:
        if not self.enemies:
            return

        self.currentActor = self.turnQueue.get_next_turn()
        
        if self.currentActor is None:
            self._end_battle()
            return

        self.upcomingTurns = self.turnQueue.get_queue_preview(count=5)

    def execute_action(self, action_cost_multiplier: float = 1.0) -> None:
        if self.currentActor is None:
            return

        if self._check_casualties():
            return

        self.turnQueue.end_turn(self.currentActor, action_cost_multiplier)
        self.start_next_turn()

    def _check_casualties(self) -> bool:
        deadEnemies = [e for e in self.enemies if getattr(e, 'dead', False)]
        
        for enemy in deadEnemies:
            self.earnedSouls += enemy.soulValue 
            xpReward = enemy.expValue
            for ally in self.party:
                ally.gain_experience(xpReward)
                
            self.enemies.remove(enemy)
            self.turnQueue.remove_entity(enemy)
            
        if not self.enemies:
            self._victory()
            return True
        
        if all(ally.dead for ally in self.party):
            self._defeat()
            return True

        return False
    
    def _victory(self) -> None:
        self.battleOver = True
        self.resultUI = BattleResultUI(
            party=self.party,
            earnedSouls=self.earnedSouls,
            victory=True,
        )

    def _defeat(self) -> None:
        self.battleOver = True
        self.resultUI = BattleResultUI(
            party=self.party,
            earnedSouls=0,
            victory=False,
        )
    def _end_battle(self) -> None:
        self.state_machine.pop()
        
    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return
    
        maxCards = 4  
        if inputId == "moveLeft":
            self.ui.selectedCardIndex = (self.ui.selectedCardIndex - 1) % maxCards
            settings.SOUNDS["select"].play()
        elif inputId == "moveRight":
            self.ui.selectedCardIndex = (self.ui.selectedCardIndex + 1) % maxCards
            settings.SOUNDS["select"].play()
        elif inputId == "enter":
            settings.SOUNDS["select"].play()
            self.execute_action(action_cost_multiplier=1.0)

    
    def render(self, surface: pygame.Surface) -> None:
        pass
     
       

   

        