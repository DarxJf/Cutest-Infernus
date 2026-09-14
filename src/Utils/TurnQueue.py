from typing import List, Optional
from src.Models.BattleEntity import BattleEntity

class TurnQueue:
    def __init__(self, entities: Optional[List[BattleEntity]] = None) -> None:
        self.entities: List[BattleEntity] = entities or []

    def add_entity(self, entity: BattleEntity) -> None:
        if entity not in self.entities:
            self.entities.append(entity)

    def remove_entity(self, entity: BattleEntity) -> None:
        if entity in self.entities:
            self.entities.remove(entity)

    def _get_active_entities(self) -> List[BattleEntity]:
        return [entity for entity in self.entities if not entity.dead]

    def get_queue_preview(self, count: int = 5) -> List[BattleEntity]:
        active = self._get_active_entities()
        if not active:
            return []

        simulatedRests = {e: e.currentRest for e in active}
        preview: List[BattleEntity] = []

        for _ in range(count):
            nextEntity = min(
                simulatedRests.keys(),
                key=lambda e: (simulatedRests[e], -e.agility)
            )
            preview.append(nextEntity)
            
            cost = nextEntity.rest / max(1, nextEntity.agility)
            simulatedRests[nextEntity] += cost

        return preview

    def get_next_turn(self) -> Optional[BattleEntity]:
        """
            The simulation advances by consuming global time until the first entity with the lowest currentRest is ready to act
        """
        active = self._get_active_entities()
        if not active:
            return None

        nextEntity = min(active, key=lambda e: (e.currentRest, -e.agility))
    
        timePassed = nextEntity.currentRest
        for entity in active:
            entity.currentRest = max(0.0, entity.currentRest - timePassed)

        return nextEntity

    def end_turn(self, entity: BattleEntity, action_cost_multiplier: float = 1.0) -> None:
        """
            Calculate and assign the new 'currentRest' to the entity at the end of their turn.
            Formula: (rest * action_multiplier) / agility
        """
        baseCost = entity.rest * action_cost_multiplier
        agilityFactor = max(1, entity.agility)
        
        entity.currentRest = baseCost / agilityFactor