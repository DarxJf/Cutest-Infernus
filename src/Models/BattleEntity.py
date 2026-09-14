from typing import Any, Dict, Callable, Set, Tuple
import random
import math

from src.Models.Entity import Entity
from src.Models.ActionCards import Action
from src.Utils.MovementCalculator import MovementCalculator
from src.Utils.AoeCalculator import AoECalculator
from src.Definitions.Entity import LEVEL_GROWTH


class BattleEntity(Entity):
    def __init__(self, definition: Dict[str, Any], x: int = 0, y: int = 0) -> None:
        super().__init__(definition, x, y)

        # position logical grid, no pixel
        self.mapX = x
        self.mapY = y

        # Flags
        self.dead = False
        self.activeStatus: dict[str, int] = {}  # {"stun": 2, "poison": 3} where the value is the remaining turns
        
        # Battle-specific attributes
        self.level            = definition.get("level", 1)
        self.classType        = definition.get("class_name", "Unknown")
        self.baseHp           = definition.get("base_hp", 10)
        self.baseAttack       = definition.get("base_attack", 5)
        self.baseMagic        = definition.get("base_magic", 5)
        self.baseAgility      = definition.get("base_agility", 5)
        self.baseDefense      = definition.get("base_defense", 5)
        self.baseMagicDefense = definition.get("base_magic_defense", 5)
        self.baseRest         = definition.get("base_rest", 3.0)  # Time to recover after action
        self.baseMovement     = definition.get("base_movement", 3)
        
        # Actions and abilities
        self.basicAttack    = definition.get("basic_attack")
        self.defaultActions = definition.get("default_actions", [])
        self.slotActions    = definition.get("slot_actions", 4)
        self.slotObjects    = definition.get("slot_objects", 1)

        # Current combat statistics
        self.hp              = self.baseHp
        self.attack          = self.baseAttack
        self.magic           = self.baseMagic
        self.agility         = self.baseAgility
        self.defense         = self.baseDefense
        self.magic_defense   = self.baseMagicDefense
        self.rest            = self.baseRest
        self.actionSlots     = [] 
        self.equippedObjects = []
        self.currentHp       = self.hp
        self.currentRest     = 0.0

        self.level           = definition.get("level", 1)
        self.experience      = definition.get("experience", 0)
        self.soulValue       = definition.get("soul_value", 10)
        self.expValue        = definition.get("exp_value", 15)
        self.experienceToNextLevel = self._calculate_xp_requirement()

    def hurt(self, amount: int) -> None:
        self.currentHp -= amount
        if self.currentHp <= 0:
            self.dead = True

    def heal(self, amount: int) -> None:
        self.currentHp += amount
        if self.currentHp > self.hp:
            self.currentHp = self.hp

    def compute_damage(self, action: "Action", target: "BattleEntity") -> int:
        variance = random.uniform(0.85, 1.15)

        if action.scalingStat == "attack":
            raw_damage = (self.attack * action.multiplier) * variance
            final_damage = math.floor(raw_damage - target.defense)

        elif action.scalingStat == "magic":
            raw_damage = (self.magic * action.multiplier) * variance
            final_damage = math.floor(raw_damage - target.magic_defense)

        elif action.scalingStat == "agility":
            raw_damage = (self.agility * action.multiplier) * variance
            final_damage = math.floor(raw_damage - target.agility)

        else:
            final_damage = 1
            
        return max(1, final_damage)

    # --------------
    # Status effects

    def apply_status(self, statusName: str, duration: int) -> None:
        self.activeStatus[statusName] = duration

    def process_status(self,) -> None:
        isStunned = False
        
        if "poison" in self.activeStatus:
            # Reutilizamos el método damage base de la clase para aplicar el veneno[cite: 1]
            self.damage(5) 
            
        if "stun" in self.activeStatus:
            isStunned = True

        # Reducir duraciones y limpiar los estados que llegaron a cero
        expired = []
        for status in self.activeStatus:
            self.activeStatus[status] -= 1
            if self.activeStatus[status] <= 0:
                expired.append(status)
                
        for status in expired:
            del self.activeStatus[status]
            
        return isStunned

    def clear_status(self) -> None:
        self.activeStatus.clear()

    # Aoe, possible moves
    def get_reachable_tiles(self, isWalkable: Callable[[int, int], bool]) -> Set[Tuple[int, int]]:
        return MovementCalculator.get_available_moves(
            self.mapX, 
            self.mapY, 
            self.baseMovement, 
            isWalkable,
        )

    def apply_aoe_damage(self, action: "Action", boardCols: int, boardRows: int, enemyList: list["BattleEntity"]) -> None:
        affectedTiles = set()

        if action.areaType == "cross":
            affectedTiles = AoECalculator.get_linear_cross(
                self.mapX, 
                self.mapY, 
                action.gridRange, 
                boardCols, 
                boardRows
            )
        elif action.areaType == "square":
            affectedTiles = AoECalculator.get_square_area(
                self.mapX, 
                self.mapY, 
                action.areaRadius, 
                boardCols, 
                boardRows
            )

        for enemy in enemyList:
            if not enemy.dead and (enemy.mapX, enemy.mapY) in affectedTiles:
                dmg = self.compute_damage(action, enemy)
                enemy.damage(dmg)


    def _calculate_xp_requirement(self) -> int:
        return self.level * self.level * 10

    def gain_experience(self, amount: int) -> bool:
        if self.dead:
            return False
            
        self.experience += amount
        leveledUp = False
       
        while self.experience >= self.experienceToNextLevel:
            self.experience -= self.experienceToNextLevel
            self._level_up()
            leveledUp = True

        return leveledUp

    def _level_up(self) -> None:
        self.level += 1
        growth = LEVEL_GROWTH.get(self.classType, LEVEL_GROWTH["Warrior"])

        self.hp            += growth["hp"]
        self.attack        += growth["attack"]
        self.magic         += growth["magic"]
        self.agility       += growth["agility"]
        self.defense       += growth["defense"]
        self.magic_defense += growth["magic_defense"]

        self.currentHp = self.hp
        self.experienceToNextLevel = self._calculate_xp_requirement()