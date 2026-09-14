from typing import List, Optional, Any
import random
import pygame

from gale.state import BaseState

from src.States.Game.SelectTargetState import SelectTargetState
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
        room,
    ) -> None:
        self.party = partyUnits
        self.enemies = enemyUnits
        self.room = room

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

        # Status
        isStunned = self.currentActor.process_status()

        if self._check_casualties():
            return

        if isStunned:
            self.turnQueue.end_turn(self.currentActor, action_cost_multiplier=1.0)
            self.start_next_turn()
            return

        self.upcomingTurns = self.turnQueue.get_queue_preview(count=5)

        if self.currentActor in self.enemies:
            self._take_enemy_turn()

    def execute_action(self, action_cost_multiplier: float = 1.0) -> None:
        if self.currentActor is None:
            return

        if self._check_casualties():
            return

        self.turnQueue.end_turn(self.currentActor, action_cost_multiplier)
        self.start_next_turn()

    def resolve_action(self, actor: BattleEntity, action: Any, targetX: int, targetY: int, is_enemy: bool) -> None:
        # Definimos quién recibe el golpe
        targets = self.party if is_enemy else self.enemies
        
        # Dimensiones del mapa (Asegúrate de pasarlas desde donde instancies Room)
        boardCols, boardRows = 20, 12 

        if action.areaType in ["cross", "square"]:
            actor.apply_aoe_damage(action, boardCols, boardRows, targets, targetX, targetY)
        else:
            for target in targets:
                if target.mapX == targetX and target.mapY == targetY and not getattr(target, 'dead', False):
                    dmg = actor.compute_damage(action, target)
                    target.damage(dmg)
                    
                    # Aplicar estados extra (veneno, stun) si la carta los tiene
                    if action.effect:
                        target.apply_status(action.effect)
                    break

        if not self._check_casualties():
            self.turnQueue.end_turn(actor, action_cost_multiplier=1.0)
            self.start_next_turn()

    def _take_enemy_turn(self) -> None:
        alive_party = [ally for ally in self.party if not getattr(ally, 'dead', False)]
        if not alive_party:
            return
            
        target = random.choice(alive_party)
        # Asumiendo que el enemigo tiene slotActions igual que el héroe
        action = random.choice(self.currentActor.slotActions)
        
        self.resolve_action(self.currentActor, action, target.mapX, target.mapY, is_enemy=True)

    def execute_action(self, action_cost_multiplier: float = 1.0) -> None:
        if self.currentActor is None or self.currentActor in self.enemies:
            return

        # 1. Tomamos la acción que el jugador seleccionó en el menú
        selected_action = self.currentActor.slotActions[self.ui.selectedCardIndex]
        
        def on_target_selected(targetX: int, targetY: int) -> None:
            # Aquí aplicamos los daños correctos y terminamos el turno
            self.resolve_action(
                self.currentActor, 
                selected_action, 
                targetX, 
                targetY, 
                is_enemy=False
            )
        
        # Congelamos el combate y empujamos el cursor a la pantalla[cite: 8]
        self.state_machine.push(
            SelectTargetState(self.state_machine),
            actor=self.currentActor,
            action=selected_action,
            enemies=self.enemies,
            callback=on_target_selected,
            boardCols=20, # O los valores que uses en tu Room
            boardRows=12
        )

    def execute_move(self) -> None:
        if self.currentActor is None or self.currentActor in self.enemies:
            return

        def on_move_selected(targetX: int, targetY: int) -> None:
            self.currentActor.mapX = targetX
            self.currentActor.logicalY = targetY
            
            # Sincronizamos los píxeles visuales para que se dibuje en el nuevo lugar
            self.currentActor.mapX = targetX * settings.TILE_SIZE
            self.currentActor.mapY = targetY * settings.TILE_SIZE
            
            # Nota: NO llamamos a self.turnQueue.end_turn() aquí, 
            # para que el menú vuelva a aparecer y le permita atacar.

        # 2. Empujamos el estado de selección a la pila (StateStack)
        self.state_machine.push(
            SelectTargetState(self.state_machine),
            actor=self.currentActor,
            action=None,  # action=None le indica al cursor que esto es un movimiento
            enemies=self.enemies,
            callback=on_move_selected,
            boardCols=20,
            boardRows=12
        )

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
     