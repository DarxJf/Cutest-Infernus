"""
Party: the 4-member team led by a main character. 
"""

from typing import List, Optional

from src.Models.BattleEntity import BattleEntity
from src.Definitions.Entity import PLAYER_CHARACTERS, get_main_characters


MAX_PARTY_SIZE = 4


class Party:
    def __init__(self, leaderKey: str) -> None:
        self.members: List[BattleEntity] = []

        mains = get_main_characters()
        if leaderKey in mains:
            self.members.append(self._create(leaderKey))

    def is_full(self) -> bool:
        return len(self.members) >= MAX_PARTY_SIZE

    def size(self) -> int:
        return len(self.members)

    def has(self, key: str) -> bool:
        return any(m.key == key for m in self.members)

    def lead(self) -> Optional[BattleEntity]:
        return self.members[0] if self.members else None

    def secondaryIndexes(self) -> List[int]:
        """Indexes of every member that is NOT the leader (i.e. index 0)."""
        return [i for i in range(1, len(self.members))]


    def hire(self, key: str, replaceIndex: Optional[int] = None) -> bool:
        """
        Hires a secondary character. If the party is full, replaceIndex
        must point to a secondary to dismiss (never the leader).
        """
        if key not in PLAYER_CHARACTERS:
            return False

        if PLAYER_CHARACTERS[key].get("role") != "secondary":
            return False  # Only secondaries can be hired

        if self.has(key):
            return False  # Already in the party

        newMember = self._create(key)

        if self.is_full():
            if replaceIndex is None or not self._canDismiss(replaceIndex):
                return False
            self.members[replaceIndex] = newMember
            return True

        self.members.append(newMember)
        return True

    def dismiss(self, index: int) -> bool:
        if not self._canDismiss(index):
            return False
        self.members.pop(index)
        return True


    def _canDismiss(self, index: int) -> bool:
        if not (0 <= index < len(self.members)):
            return False
        if index == 0:
            return False  
        return True

    def _create(self, key: str) -> BattleEntity:
        member = BattleEntity(definition=PLAYER_CHARACTERS[key], x=0, y=0)
        member.key = key   
        return member