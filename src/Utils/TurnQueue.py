"""
Turn order for the battle, organized by rounds.

"""

from typing import List, Optional

from src.Models.BattleEntity import BattleEntity


class TurnQueue:
    def __init__(self, entities: Optional[List[BattleEntity]] = None) -> None:
        self.entities: List[BattleEntity] = entities or []

        self.roundOrder: List[BattleEntity] = []
        self.currentIndex: int = 0

    def add_entity(self, entity: BattleEntity) -> None:
        if entity not in self.entities:
            self.entities.append(entity)

    def remove_entity(self, entity: BattleEntity) -> None:
        if entity in self.entities:
            self.entities.remove(entity)
        self.roundOrder = [e for e in self.roundOrder if e is not entity]


    def _get_active_entities(self) -> List[BattleEntity]:
        return [e for e in self.entities if not e.dead]

    def rebuild_round(self) -> None:
      
        active = self._get_active_entities()
        self.roundOrder = sorted(active, key=lambda e: -e.agility)
        self.currentIndex = 0

    def peek_current(self) -> Optional[BattleEntity]:
       
        while self.currentIndex < len(self.roundOrder):
            entity = self.roundOrder[self.currentIndex]
            if entity.dead:
                self.currentIndex += 1
                continue
            return entity
        return None

    def get_next_turn(self) -> Optional[BattleEntity]:
    
        entity = self.peek_current()
        if entity is None:
            self.rebuild_round()
            entity = self.peek_current()
            if entity is None:
                return None

        self.currentIndex += 1
        return entity

    def end_turn(
        self,
        entity: BattleEntity,
        action_cost_multiplier: float = 1.0,
    ) -> None:
     
        pass

    def get_queue_preview(self, count: int = 5) -> List[BattleEntity]:
        
        preview: List[BattleEntity] = []
        startIdx = max(0, self.currentIndex - 1)
        idx = startIdx

        while idx < len(self.roundOrder) and len(preview) < count:
            entity = self.roundOrder[idx]
            if not entity.dead:
                preview.append(entity)
            idx += 1

        return preview

    def is_round_complete(self) -> bool:
        return self.currentIndex >= len(self.roundOrder)