from typing import Set, Tuple, Callable, Any

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
        
        availableMoves: Set[Tuple[int, int]] = set()
        queue = [(startX, startY, 0)]
        visited: Set[Tuple[int, int]] = {(startX, startY)}
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        while queue:
            cx, cy, steps = queue.pop(0)
            availableMoves.add((cx, cy))
            
            if steps < rangeLimit:
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if (nx, ny) not in visited and isWalkable(nx, ny):
                        visited.add((nx, ny))
                        queue.append((nx, ny, steps + 1))
                        
        return availableMoves

    @staticmethod
    def get_path_to_target( # return a path to ai
        startX: int, 
        startY: int, 
        targetX: int, 
        targetY: int, 
        isWalkable: Callable[[int, int], bool]
    ) -> list[Tuple[int, int]]:
        
        def grid_successors(state: Tuple[int, int]):
            cx, cy = state
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                # A tile is a valid successor if it is walkable
                if isWalkable(nx, ny):
                    # yield (next_state, cost, action_label)
                    yield (nx, ny), 1, (dx, dy)

        start = (startX, startY)
        target = (targetX, targetY)

        graph = StateGraph.expand(start, grid_successors)
        solution = breadth_first_search(start, target, graph)

        if solution is None:
            return []  # No path found

        return list(solution)  # Convert the generator to a list of coordinates

    @staticmethod
    def create_walkable_func( # To check if an entity occuped a tile
        room_is_walkable: Callable[[int, int], bool],
        entities: list,
        ignore_entities: Any = None
    ) -> Callable[[int, int], bool]:
        if ignore_entities is None:
            ignore_entities = []
        elif not isinstance(ignore_entities, (list, tuple, set)):
            ignore_entities = [ignore_entities]

        def checker(x: int, y: int) -> bool:
            if not room_is_walkable(x, y):
                return False
                
            for entity in entities:
                if entity not in ignore_entities and not getattr(entity, 'dead', False):
                    if entity.mapX == x and entity.mapY == y:
                        return False # Casilla ocupada
            return True
            
        return checker
