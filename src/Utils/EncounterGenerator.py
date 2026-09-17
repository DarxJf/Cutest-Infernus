"""
Builds the enemy horde for a battle, scaling with the run's progress.
"""

import random
from typing import Any, Dict, List

from src.Definitions.Entity import ENEMIES

MAX_HORDE_SIZE = 5

def _enemy_pool_for(battlesFought: int) -> List[str]:
    if battlesFought <= 1:
        return ["slime"]

    if battlesFought <= 2:
        return ["slime", "skeleton", "skeleton"]

    if battlesFought <= 3:
        return ["skeleton", "skeleton", "demon"]

    return ["slime", "skeleton", "skeleton", "demon", "demon"]


def _horde_size_for(battlesFought: int) -> int:
    base = 2 + battlesFought // 2
    return min(base, MAX_HORDE_SIZE)


def _level_bonus_for(battlesFought: int) -> int:
    return min(battlesFought // 3, 5)


def generate_horde(battlesFought: int) -> List[Dict[str, Any]]:
    pool = _enemy_pool_for(battlesFought)
    size = _horde_size_for(battlesFought)
    levelBonus = _level_bonus_for(battlesFought)

    chosen = [random.choice(pool) for _ in range(size)]

    horde: List[Dict[str, Any]] = []
    for key in chosen:
        baseDef = ENEMIES[key]
        scaled = dict(baseDef)  

        scaled["class_name"] = baseDef["class_name"]
        scaled["level"] = baseDef.get("level", 1) + levelBonus

        if levelBonus > 0:
            scaled["base_hp"] = baseDef["base_hp"] + levelBonus * 5
            scaled["base_attack"] = baseDef["base_attack"] + levelBonus * 2
            scaled["base_defense"] = baseDef["base_defense"] + levelBonus

        horde.append(scaled)

    return horde