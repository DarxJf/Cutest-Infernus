from typing import Any, Dict, Callable, Set, Tuple

import settings
from src.Models.Entity import Entity
from src.Utils.MovementCalculator import MovementCalculator

class BattleEntity(Entity):
    def __init__(self, definition: Dict[str, Any], x: int = 0, y: int = 0) -> None:
        super().__init__(definition, x, y)

        # position logical grid, no pixel
        self.mapX = x
        self.mapY = y

        # Flags
        self.dead = False
        
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

    def hurt(self, amount: int) -> None:
        self.currentHp -= amount
        if self.currentHp <= 0:
            self.dead = True

    def heal(self, amount: int) -> None:
        self.currentHp += amount
        if self.currentHp > self.hp:
            self.currentHp = self.hp

    def get_reachable_tiles(self, isWalkable: Callable[[int, int], bool]) -> Set[Tuple[int, int]]:
        """Requests reachable grid coordinates based on fixed base_movement."""
        print("\n--- DEBUG ALGORITMO ---")
        print(f"1. Coordenadas lógicas de inicio: ({self.mapX}, {self.mapY})")
        print(f"2. Rango de movimiento (baseMovement): {self.baseMovement}")
        print(f"3. Casilla derecha ({self.mapX + 1}, {self.mapY}) es caminable?: {isWalkable(self.mapX + 1, self.mapY)}")
        print("-----------------------\n")
        return MovementCalculator.get_available_moves(
            self.mapX, 
            self.mapY, 
            self.baseMovement, 
            isWalkable,
        )