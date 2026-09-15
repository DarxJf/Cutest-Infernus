from typing import List, Optional, Any
import random
import pygame
import time

from gale.state import BaseState

from src.States.Game.SelectTargetState import SelectTargetState
import settings
from src.Utils.TurnQueue import TurnQueue
from src.Models.BattleEntity import BattleEntity
from src.Gui.BatleUI import BattleUI
from src.Gui.BatleResultUI import BattleResultUI
from src.ai.BehaviorEnemy import build_enemy_brain


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
        self.enemy_brain = build_enemy_brain()

        allUnits = self.party + self.enemies
        self.turnQueue = TurnQueue(allUnits)

        self.ui = BattleUI()
        
        self.currentActor = None
        self.upcomingTurns = []

        self.earnedSouls = 0
        self.battleOver = False      
        self.resultUI = None 

        # glow
        self.glowSurface = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(
            self.glowSurface, 
            (0, 150, 255, 128), 
            (0, 0, settings.TILE_SIZE, settings.TILE_SIZE)
        )

        # self.rangeSurface = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA)
        # pygame.draw.rect(self.rangeSurface, (255, 50, 50, 100), (0, 0, settings.TILE_SIZE, settings.TILE_SIZE))

        self.currentGlow = self.glowSurface
        
        self.start_next_turn()

    def start_next_turn(self) -> None:
        if not self.enemies:
            return

        self.currentActor = self.turnQueue.get_next_turn()

        self.hasMoved = False
        
        if self.currentActor is None:
            self._end_battle()
            return

        # Status
        isStunned = self.currentActor.process_status()
        self.currentActor.process_cooldowns()

        if self._check_casualties():
            return

        if isStunned:
            self.turnQueue.end_turn(self.currentActor, action_cost_multiplier=1.0)
            self.start_next_turn()
            return

        self.upcomingTurns = self.turnQueue.get_queue_preview(count=5)

        if self.currentActor in self.enemies:
            self._take_enemy_turn()

    def resolve_action(self, actor: BattleEntity, action: Any, targetX: int, targetY: int, is_enemy: bool) -> None:
        if action.targetType == "self":
            targets = [actor]
        elif action.targetType == "ally":
            targets = self.enemies if is_enemy else self.party
        else: # "enemy"
            targets = self.party if is_enemy else self.enemies

        boardCols, boardRows = self.room.cols, self.room.rows 

        if action.areaType in ["cross", "square"]:
            actor.apply_aoe_damage(action, boardCols, boardRows, self.enemies)
        else:
            for target in targets:
                if target.mapX == targetX and target.mapY == targetY and not getattr(target, 'dead', False):
                    distance = abs(target.mapX - actor.mapX) + abs(target.mapY - actor.mapY)

                    if distance <= action.gridRange or action.targetType == "self":
                        dmg = actor.compute_damage(action, target)

                        if action.effect == "heal":
                            target.heal(amount=dmg)
                        else:
                            target.hurt(dmg)
                            if action.effect:
                                target.apply_status(action.effect, 1)

                    else:
                        print(f"Fallo: ¡El objetivo está a {distance} casillas, el arma solo alcanza {action.gridRange}!")
                    break

        if action.cooldown > 0:
            actor.skillCooldowns[action.name] = action.cooldown

        if not self._check_casualties():
            self.turnQueue.end_turn(actor, action_cost_multiplier=1.0)
            self.start_next_turn()

    def _take_enemy_turn(self) -> None:
        alive_party = [ally for ally in self.party if not getattr(ally, 'dead', False)]
        if not alive_party:
            return

        self.enemy_brain.tick(self, 0)

        if getattr(self, 'hasMoved', False) and self.currentActor in self.enemies:
            self.enemy_brain.tick(self, 0)

    def execute_action(self, action_cost_multiplier: float = 1.0) -> None:
        if self.currentActor is None or self.currentActor in self.enemies:
            return

        if self.ui.selectedCardIndex == 1:
            selected_action = self.currentActor.basicAttack
        else:
            list_index = self.ui.selectedCardIndex - 2
            selected_action = self.currentActor.actionSlots[list_index]

        if selected_action.name in self.currentActor.skillCooldowns:
            print(f"¡{selected_action.name} está en enfriamiento!")
            return
        
        def on_target_selected(targetX: int, targetY: int) -> None:
            self.resolve_action(
                self.currentActor, 
                selected_action, 
                targetX, 
                targetY, 
                is_enemy=False
            )

        targetGroup = self.party if selected_action.targetType in ["ally", "self"] else self.enemies

        self.state_machine.push(
            SelectTargetState(self.state_machine),
            actor=self.currentActor,
            action=selected_action,
            enemies=targetGroup,
            callback=on_target_selected,
            boardCols=20,
            boardRows=12,
            offsetX=self.room.offsetX,
            offsetY=self.room.offsetY,
            glowSurface=self.glowSurface
        )

    def execute_move(self) -> None:
        if self.currentActor is None or self.currentActor in self.enemies:
            return

        if getattr(self, 'hasMoved', False):
            print("¡Ya te has movido en este turno!")
            return

        reachable = self.currentActor.get_reachable_tiles(self.room.is_walkable)
    
        self.reachableTiles = reachable
    
        def on_test_target_selected(targetX: int, targetY: int) -> None:
            self.currentActor.mapX = targetX
            self.currentActor.mapY = targetY
    
            print(f"Posiciones logicas nuevas: {self.currentActor.mapX} , {self.currentActor.mapY}")
    
            self.currentActor.x = targetX * settings.TILE_SIZE
            self.currentActor.y = targetY * settings.TILE_SIZE
    
            self.reachableTiles = set()

            self.hasMoved = True
    
        self.state_machine.push(
            SelectTargetState(self.state_machine),
            actor=self.currentActor,
            action=None,
            enemies=self.enemies,
            callback=on_test_target_selected,
            boardCols=self.room.cols,
            boardRows=self.room.rows,
            validTiles=reachable,
            offsetX=self.room.offsetX,
            offsetY=self.room.offsetY
        )

    def _check_casualties(self) -> bool:
        deadEnemies = [e for e in self.enemies if getattr(e, 'dead', False)]
        
        for enemy in deadEnemies:
            self.earnedSouls += enemy.soulValue 
            xpReward = enemy.expValue
            for ally in self.party:
                ally.gain_experience(xpReward, ally.classType)
                
            self.enemies.remove(enemy)
            self.turnQueue.remove_entity(enemy)
            
        if not self.enemies:
            self._victory()
            return True
        
        if all(ally.dead for ally in self.party):
            self._defeat()
            return True

        return False

    def _glow_tile(self, surface: pygame.Surface, gridX: int, gridY: int, offsetX, offsetY) -> None:
        pixelX = gridX * settings.TILE_SIZE + offsetX
        pixelY = gridY * settings.TILE_SIZE + offsetY
        surface.blit(self.currentGlow, (pixelX, pixelY))
    
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

        if self.battleOver:
            if inputId == "enter":
                settings.SOUNDS["select"].play()
                self._end_battle() 
            return
    
        maxCards = 3 + len(self.currentActor.actionSlots)
        if inputId == "moveLeft":
            self.ui.selectedCardIndex = (self.ui.selectedCardIndex - 1) % maxCards
            settings.SOUNDS["select"].play()
        elif inputId == "moveRight":
            self.ui.selectedCardIndex = (self.ui.selectedCardIndex + 1) % maxCards
            settings.SOUNDS["select"].play()
        elif inputId == "enter":
            settings.SOUNDS["select"].play()

            if self.ui.selectedCardIndex == 0:
                self.execute_move()
            elif self.ui.selectedCardIndex == maxCards - 1:
                self.turnQueue.end_turn(self.currentActor, action_cost_multiplier=1.0)
                self.start_next_turn()
            else:
                self.execute_action(action_cost_multiplier=1.0)

    def update(self, dt):
        self.room.update(dt)

        for enemy in self.enemies:
            enemy.update(dt)
        
    def render(self, surface: pygame.Surface) -> None:
        # render Glow
        if hasattr(self, 'reachableTiles') and self.reachableTiles:
            for gridX, gridY in self.reachableTiles:
                self._glow_tile(surface, gridX, gridY, self.room.offsetX, self.room.offsetY)

        hasMoved = getattr(self, 'hasMoved', False)
        self.ui.render(surface, self.currentActor, self.upcomingTurns, hasMoved)

        if self.battleOver and self.resultUI:
            self.resultUI.render(surface)
     