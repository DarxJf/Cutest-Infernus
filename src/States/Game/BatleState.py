from typing import List, Optional, Any
import random
import pygame
import time

from gale.state import BaseState

import settings
from src.ai.BehaviorEnemy import build_enemy_brain
from src.Definitions.Texts import BATTLE_START_TEXT, BOSS_START_TEXT
from src.Gui.BatleUI import BattleUI
from src.Gui.BatleResultUI import BattleResultUI
from src.Models.BattleEntity import BattleEntity
from src.Utils.TurnQueue import TurnQueue
from src.Utils.MovementCalculator import MovementCalculator
from src.Utils.SpawnHelper import find_free_tiles, find_free_tile
from src.States.Game.RunState import RunState
from src.States.Game.GameOverState import GameOverState
from src.States.Game.RestState import RestState
from src.States.Game.DialogueState import DialogueState
from src.States.Game.SelectTargetState import SelectTargetState


EFFECTS = {
    "poison": 3,
    "stun": 1,
}


class BattleState(BaseState):
    def enter(
        self,
        runState: RunState,
        enemies: List[BattleEntity],
        room,
        isBoss: bool = False, 
    ) -> None:
        self.runState = runState
        self.party = runState.party.members
        self.enemies = enemies
        self.room = room
        self.isBoss = isBoss

        self._place_party()
        self._place_enemies()
        self._mark_party_flags()

        self.enemy_brain = {enemy: build_enemy_brain() for enemy in self.enemies}

        self.allUnits = self.party + self.enemies
        self.turnQueue = TurnQueue(self.allUnits)
        self.turnQueue.rebuild_round()

        self.pendingEnemyTurn = False
        self.enemyTurnDelay = 0.0

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

        self.currentGlow = self.glowSurface

        if self.isBoss:
            starText = BOSS_START_TEXT
        else: 
            starText = BATTLE_START_TEXT

                   
        self.state_machine.push(
            DialogueState(self.state_machine),
            text=starText,
            position = "bottom",
        )
         
        self.start_next_turn()

    def _place_party(self) -> None:
        anchor = (3, self.room.rows - 3)

        offsets = [
            (0, 0), (-1, 0), (0, -1), (-1, -1), (0, -2), (-1, -2),
        ]

        occupied = set()
        tiles = find_free_tiles(
            self.room, anchor, len(self.party), occupied, offsets,
        )

        for member, tile in zip(self.party, tiles):
            member.mapX, member.mapY = tile
            member.x = tile[0] * settings.TILE_SIZE
            member.y = tile[1] * settings.TILE_SIZE

    def _place_enemies(self) -> None:
        anchor = (self.room.cols - 4, 3)

        offsets = [
            (0, 0), (-1, 0), (-2, 0),
            (0, 1), (-1, 1), (-2, 1),
            (0, 2), (-1, 2), (-2, 2),
        ]

        occupied = set()
        tiles = find_free_tiles(
            self.room, anchor, len(self.enemies), occupied, offsets,
        )

        for enemy, tile in zip(self.enemies, tiles):
            enemy.mapX, enemy.mapY = tile
            enemy.x = tile[0] * settings.TILE_SIZE
            enemy.y = tile[1] * settings.TILE_SIZE

    def _mark_party_flags(self) -> None:
        for member in self.party:
            member.is_party = True
        for enemy in self.enemies:
            enemy.is_party = False

    def start_next_turn(self) -> None:
        self.ui.selectedCardIndex = 0

        if self.runState.is_game_over():
            self._defeat()
            return
        
        if not self.enemies:
            return

        self.currentActor = self.turnQueue.get_next_turn()

        self.hasMoved = False
        
        if self.currentActor is None:
            self._end_battle()
            return

        self.ui.selectedCardIndex = 0

        # Status
        isStunned = self.currentActor.process_status()
        self.currentActor.process_cooldowns()

        if getattr(self.currentActor, "dead", False):
            self.start_next_turn()
            return

        if self._check_casualties():
            return

        if isStunned:
            self.start_next_turn()
            return

        self.upcomingTurns = self.turnQueue.get_queue_preview(count=10)

        if self.currentActor in self.enemies:
            self.pendingEnemyTurn = True
            self.enemyTurnDelay = 2

    def resolve_action(self, actor: BattleEntity, action: Any, targetX: int, targetY: int, is_enemy: bool) -> None:
        if action.targetType == "self":
            targets = [actor]
        elif action.targetType == "ally":
            targets = self.enemies if is_enemy else self.party
        else: # "enemy"
            targets = self.party if is_enemy else self.enemies

        boardCols, boardRows = self.room.cols, self.room.rows 

        actor.state_machine.change("attack", actor, targetX, targetY)

        if action.areaType in ["cross", "square"]:
            actor.apply_aoe_damage(action, boardCols, boardRows, targets)
        else:
            for target in targets:
                if target.mapX == targetX and target.mapY == targetY and not getattr(target, 'dead', False):
                    # NUEVO: Lógica condicional para ataques "single" vs otros
                    dx = abs(target.mapX - actor.mapX)
                    dy = abs(target.mapY - actor.mapY)
                    
                    if action.areaType == "single":
                        distance = max(dx, dy)
                    else:
                        distance = dx + dy

                    if distance <= action.gridRange or action.targetType == "self":
                        dmg = actor.compute_damage(action, target)

                        if action.effect == "heal":
                            target.heal(amount=dmg)
                        else:
                            target.hurt(dmg)
                            if action.effect:
                                target.apply_status(action.effect, EFFECTS[action.effect])
                    else:
                        print(f"Fallo: ¡El objetivo está a {distance} casillas, el arma solo alcanza {action.gridRange}!")
                    break

        if action.cooldown > 0:
            actor.skillCooldowns[action.name] = action.cooldown

        if not self._check_casualties():
            self.start_next_turn()

    def _take_enemy_turn(self) -> None:
        if self.battleOver:
            return
        if self.currentActor not in self.enemies:
            return
        
        alive_party = [ally for ally in self.party if not getattr(ally, 'dead', False)]
        if not alive_party:
            return

        brain = self.enemy_brain[self.currentActor]

        brain.tick(self, 0)

        if getattr(self, 'hasMoved', False) and self.currentActor in self.enemies:
            brain.tick(self, 0)

    def execute_action(self, action_cost_multiplier: float = 1.0) -> None:
        if self.currentActor is None or self.currentActor in self.enemies:
            return

        if self.ui.selectedCardIndex == 1:
            selected_action = self.currentActor.basicAttack
        else:
            list_index = self.ui.selectedCardIndex - 2
            selected_action = self.currentActor.actionSlots[list_index]

        if selected_action.name in self.currentActor.skillCooldowns:
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
            return

        walkable_func = MovementCalculator.create_walkable_func(
            self.room.is_walkable,
            self.allUnits,
            ignore_entities=self.currentActor,
        )

        reachable = self.currentActor.get_reachable_tiles(isWalkable=walkable_func)
    
        self.reachableTiles = reachable
    
        def on_test_target_selected(targetX: int, targetY: int) -> None:
            # self.currentActor.mapX = targetX
            # self.currentActor.mapY = targetY

            # self.currentActor.x = targetX * settings.TILE_SIZE
            # self.currentActor.y = targetY * settings.TILE_SIZE
    
            self.reachableTiles = set()

            self.currentActor.state_machine.change("walk", self.currentActor, targetX, targetY)

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
        
        if self.runState.is_game_over():
            self._defeat()
            return True

        return False

    def _glow_tile(self, surface: pygame.Surface, gridX: int, gridY: int, offsetX, offsetY) -> None:
        pixelX = gridX * settings.TILE_SIZE + offsetX
        pixelY = gridY * settings.TILE_SIZE + offsetY
        surface.blit(self.currentGlow, (pixelX, pixelY))
    
    def _victory(self) -> None:
        self.battleOver = True
        self.runState.register_battle_won() 
        self.runState.wallet.earn(self.earnedSouls)

        self.resultUI = BattleResultUI(
            party=self.party,
            earnedSouls=self.earnedSouls,
            victory=True,
        )

        if self.isBoss:
            message = "BOSS DEFEATED!"
            self.state_machine.push(
                DialogueState(self.state_machine),
                text=message,
                position="bottom",
            )

    def _defeat(self) -> None:
        self.battleOver = True
        self.resultUI = BattleResultUI(
            party=self.party,
            earnedSouls=0,
            victory=False,
        )

    def _end_battle(self) -> None:
        for e in self.party:
            e.process_cooldowns()

        if self.resultUI is None:
            self.state_machine.pop()
            return
        
        victory = self.resultUI.victory

        self.state_machine.pop()

        if self.runState.is_game_over():
            self.state_machine.push(GameOverState(self.state_machine))
            return

        elif victory:
            self.state_machine.push(
                RestState(self.state_machine),
                runState=self.runState,
            )
        
    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return

        if inputId == "pause":
            from src.States.Game.PauseMenuState import PauseMenuState
            self.state_machine.push(
            PauseMenuState(self.state_machine),
            runState=self.runState,
            inBattle=True,
            )
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
                self.start_next_turn()
            else:
                self.execute_action(action_cost_multiplier=1.0)

    def update(self, dt):
        self.room.update(dt)
        for entity in self.allUnits:
            entity.update(dt)

        if getattr(self, "pendingEnemyTurn", False):
            self.enemyTurnDelay -= dt
            if self.enemyTurnDelay <= 0:
                self.pendingEnemyTurn = False
                self._take_enemy_turn()
        
    def render(self, surface: pygame.Surface) -> None:
        self.room.render(surface)

        offsetX = self.room.offsetX
        offsetY = self.room.offsetY

        # render Glow
        if hasattr(self, 'reachableTiles') and self.reachableTiles:
            for gridX, gridY in self.reachableTiles:
                self._glow_tile(surface, gridX, gridY, self.room.offsetX, self.room.offsetY)

        hasMoved = getattr(self, 'hasMoved', False)
        self.ui.render(surface, self.currentActor, self.upcomingTurns, hasMoved)

        for entity in self.party:
            entity.render(surface, offsetX, offsetY)

        for enemy in self.enemies:
            enemy.render(surface, offsetX, offsetY)
     
        if self.battleOver and self.resultUI:
            self.resultUI.render(surface)
     