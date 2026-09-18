"""
Party: the 4-member team led by a main character. 
"""

from typing import List, Optional, Any, Dict

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
        if not self.members:
            return None
        leader = self.members[0]
        return None if leader.dead else leader
    
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
        leader = self.lead()
        if leader is not None:
            targetLevel = max(1, leader.level - 1)
            for _ in range(targetLevel - newMember.level):
                newMember._level_up(newMember.classType)

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

    def to_dict(self) -> Dict[str, Any]:
   
        return {
            "members": [
                {
                    "key": m.key,
                    "level": m.level,
                    "hp": m.hp,
                    "attack": m.attack,
                    "magic": m.magic,
                    "agility": m.agility,
                    "defense": m.defense,
                    "magic_defense": m.magic_defense,
                    "currentHp": m.currentHp,
                    "experience": m.experience,
                    "experienceToNextLevel": m.experienceToNextLevel,
                    "dead": m.dead,
                }
                for m in self.members
            ],
        }

    def load_dict(self, data: Dict[str, Any]) -> None:
        self.members = []

        for memberData in data.get("members", []):
            key = memberData["key"]
            if key not in PLAYER_CHARACTERS:
                continue  

            member = self._create(key)

            member.level = memberData.get("level", member.level)
            member.hp = memberData.get("hp", member.hp)
            member.attack = memberData.get("attack", member.attack)
            member.magic = memberData.get("magic", member.magic)
            member.agility = memberData.get("agility", member.agility)
            member.defense = memberData.get("defense", member.defense)
            member.magic_defense = memberData.get(
                "magic_defense", member.magic_defense,
            )
            member.currentHp = memberData.get("currentHp", member.hp)
            member.experience = memberData.get("experience", 0)
            member.experienceToNextLevel = memberData.get(
                "experienceToNextLevel", member.experienceToNextLevel,
            )
            member.dead = memberData.get("dead", False)

            self.members.append(member)