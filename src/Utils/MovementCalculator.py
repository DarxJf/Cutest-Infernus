from typing import Set, Tuple, Callable
from gale.ai.graph import StateGraph
from gale.ai.search import breadth_first_search

class MovementCalculator:
    @staticmethod
    def get_available_moves(
        startX: int, 
        startY: int, 
        rangeLimit: int, 
        isWalkable: Callable[[int, int], bool]
    ) -> Set[Tuple[int, int]]:
        
        available = set()
        
        # here will create a graph
        available.add((startX, startY))
        
        return available