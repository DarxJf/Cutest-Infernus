from typing import Any, Dict, Callable, Set, Tuple
import random
import math

from src.Definitions.ActionCards import BASIC_ATTACK_DEF, UNIVERSAL_ACTIONS,  WARRIOR_ACTIONS,  ROGUE_ACTIONS,  FAIRY_ACTIONS,  MAGE_ACTIONS,  ENEMY_ACTIONS
from src.Models.Entity import Entity
from src.Models.ActionCards import Action
from src.Utils.MovementCalculator import MovementCalculator
from src.Utils.AoeCalculator import AoECalculator
from src.Definitions.Entity import LEVEL_GROWTH

from src.States.Entity.IdleState import EntityIdleState
from src.States.Entity.WalkState import EntityWalkState
from src.States.Entity.AttackState import EntityAttackState


ALL_ACTIONS = {
    **BASIC_ATTACK_DEF,
    **UNIVERSAL_ACTIONS, 
    **WARRIOR_ACTIONS, 
    **ROGUE_ACTIONS, 
    **FAIRY_ACTIONS, 
    **MAGE_ACTIONS, 
    **ENEMY_ACTIONS,
}

class BattleEntity(Entity):
    def __init__(self, definition: Dict[str, Any], x: int = 0, y: int = 0) -> None:
        super().__init__(definition, x, y)

        # position logical grid, no pixel
        self.mapX = x
        self.mapY = y

        # Flags, structs, etc.
        self.dead = False
        self.activeStatus: dict[str, int] = {}  # {"stun": 2, "poison": 3} where the value is the remaining turns
        self.skillCooldowns: dict[str, int] = {}
        self.facing: str = "down"
        
        # Battle-specific attributes
        self.name             = definition.get("name", "Snow")
        self.level            = definition.get("level", 1)
        self.classType        = definition.get("class_name", "Warrior")
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
        self.basicAttack     = Action("basic_strike", BASIC_ATTACK_DEF)
        self.actionSlots     = []
        for key in self.defaultActions:
            if key in ALL_ACTIONS:
                newAction = Action(key, ALL_ACTIONS[key])
                self.actionSlots.append(newAction) 
        self.equippedObjects = []
        self.currentHp       = self.hp
        self.currentRest     = 0.0

        self.level           = definition.get("level", 1)
        self.experience      = definition.get("experience", 0)
        self.soulValue       = definition.get("soul_value", 10)
        self.expValue        = definition.get("exp_value", 15)

        self.experienceToNextLevel = self._calculate_xp_requirement()

        # State machine
        self.state_machine.states = {
            "idle"  : EntityIdleState,
            "walk"  : EntityWalkState,
            "attack": EntityAttackState,
        }

        self.state_machine.change("idle", self)

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
            self.hurt(5) 
            
        if "stun" in self.activeStatus:
            isStunned = True

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

    # cooldowns
    def process_cooldowns(self) -> None:
        expired = []
        for skillName in self.skillCooldowns:
            self.skillCooldowns[skillName] -= 1
            if self.skillCooldowns[skillName] <= 0:
                expired.append(skillName)

        for skillName in expired:
            del self.skillCooldowns[skillName]

    # Aoe, possible moves
    def get_reachable_tiles(self, isWalkable: Callable[[int, int], bool]) -> Set[Tuple[int, int]]:
        return MovementCalculator.get_available_moves(
            self.mapX, 
            self.mapY, 
            self.baseMovement, 
            isWalkable,
        )

    def apply_aoe_damage(self, action: "Action", boardCols: int, boardRows: int, targetList: list["BattleEntity"]) -> None:
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

        for target in targetList:
            if not target.dead and (target.mapX, target.mapY) in affectedTiles:
                dmg = self.compute_damage(action, target)

                if action.effect == "heal":
                    target.heal(dmg)
                else:
                    target.hurt(dmg)


    def _calculate_xp_requirement(self) -> int:
        return self.level * self.level * 10

    def gain_experience(self, amount: int, classType: str) -> bool:
        if self.dead:
            return False
            
        self.experience += amount
        leveledUp = False
       
        while self.experience >= self.experienceToNextLevel:
            self.experience -= self.experienceToNextLevel
            self._level_up(classType)
            leveledUp = True

        return leveledUp

    def _level_up(self, classType: str) -> None:
        self.level += 1
        growth = LEVEL_GROWTH.get(self.classType, LEVEL_GROWTH[classType])

        self.hp            += growth["hp"]
        self.attack        += growth["attack"]
        self.magic         += growth["magic"]
        self.agility       += growth["agility"]
        self.defense       += growth["defense"]
        self.magic_defense += growth["magic_defense"]

        self.currentHp = self.hp
        self.experienceToNextLevel = self._calculate_xp_requirement()