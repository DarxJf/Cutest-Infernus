"""
Shared inventory: stores passive objects and tracks which party member
(if any) has each one equipped.
"""

from typing import Any, Dict, List, Optional

from src.Models.BattleEntity import BattleEntity
from src.Models.Objects import PassiveObject
from src.Definitions.Objects import PASSIVE_OBJECTS


class Inventory:
    def __init__(self) -> None:
        self.items: Dict[str, PassiveObject] = {}

        self.equipped: Dict[int, List[str]] = {}

    def add(self, objectKey: str) -> bool:
        if objectKey not in PASSIVE_OBJECTS:
            return False
        if objectKey in self.items:
            return False  

        self.items[objectKey] = PassiveObject(objectKey, PASSIVE_OBJECTS[objectKey])
        return True

    def has(self, objectKey: str) -> bool:
        return objectKey in self.items

    def all_keys(self) -> List[str]:
        return list(self.items.keys())


    def equip(
        self,
        objectKey: str,
        memberIndex: int,
        member: BattleEntity,
    ) -> bool:
        """
        Equips an object on a party member, respecting their slot cap.
        Unequips any existing item in that slot first (1 slot default).
        """
        if objectKey not in self.items:
            return False

        slotCap = getattr(member, "slotObjects", 1)
        equippedNow = self.equipped.setdefault(memberIndex, [])

        if len(equippedNow) >= slotCap:
            self.unequip(equippedNow[0], memberIndex, member)

        obj = self.items.pop(objectKey)
        obj.equip_object(member)
        self.equipped[memberIndex].append(objectKey)
        return True

    def unequip(
        self,
        objectKey: str,
        memberIndex: int,
        member: BattleEntity,
    ) -> bool:
        equippedNow = self.equipped.get(memberIndex, [])

        if objectKey not in equippedNow:
            return False

        obj = PassiveObject(objectKey, PASSIVE_OBJECTS[objectKey])
        obj.unequip_object(member)
        equippedNow.remove(objectKey)
        self.items[objectKey] = obj
        return True

    def equipped_keys_for(self, memberIndex: int) -> List[str]:
        return list(self.equipped.get(memberIndex, []))