"""
Helpers to find free, walkable tiles on the board. Used by PlayState to
place the party and by BattleState to place both party and enemies
without ever overlapping rocks, walls, or other units.
"""

from typing import List, Optional, Sequence, Set, Tuple

from src.Models.Room import Room


def is_tile_free(
    room: Room,
    x: int,
    y: int,
    occupied: Set[Tuple[int, int]],
) -> bool:
    if not room.is_walkable(x, y):
        return False
    if (x, y) in occupied:
        return False
    return True


def find_free_tile(
    room: Room,
    preferredX: int,
    preferredY: int,
    occupied: Set[Tuple[int, int]],
    maxRadius: int = 6,
) -> Optional[Tuple[int, int]]:
   
    if is_tile_free(room, preferredX, preferredY, occupied):
        return (preferredX, preferredY)

    for radius in range(1, maxRadius + 1):
        for dx in range(-radius, radius + 1):
            for dy in (-radius, radius):
                for (x, y) in (
                    (preferredX + dx, preferredY + dy),
                    (preferredX + dy, preferredY + dx),
                ):
                    if is_tile_free(room, x, y, occupied):
                        return (x, y)
    return None


def find_free_tiles(
    room: Room,
    anchor: Tuple[int, int],
    count: int,
    occupied: Set[Tuple[int, int]],
    order: Sequence[Tuple[int, int]],
) -> List[Tuple[int, int]]:
   
    result: List[Tuple[int, int]] = []
    ax, ay = anchor

    for dx, dy in order:
        if len(result) >= count:
            break
        x, y = ax + dx, ay + dy
        if is_tile_free(room, x, y, occupied):
            result.append((x, y))
            occupied.add((x, y))

    while len(result) < count:
        tile = find_free_tile(room, ax, ay, occupied)
        if tile is None or tile in result:
            break
        result.append(tile)
        occupied.add(tile)

    return result