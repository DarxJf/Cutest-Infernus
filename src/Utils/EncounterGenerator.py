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

def generate_boss_encounter(battlesFought: int, bossesDefeated: int = 0) -> List[Dict[str, Any]]:
    """
    Boss encounter: one boss plus 2 minions. The boss scales with
    BOTH the general battle count and the number of bosses already
    killed, so each cycle is meaningfully harder.
    """
    bossDef = ENEMIES["boss"]

    levelBonus = _level_bonus_for(battlesFought) + bossesDefeated * 2

    boss = dict(bossDef)
    boss["level"] = bossDef.get("level", 1) + levelBonus
    boss["base_hp"] = bossDef["base_hp"] + levelBonus * 10
    boss["base_attack"] = bossDef["base_attack"] + levelBonus * 2
    boss["base_defense"] = bossDef["base_defense"] + levelBonus
    boss["base_magic"] = bossDef.get("base_magic", 0) + levelBonus

    pool = _enemy_pool_for(battlesFought)
    minionKeys = [random.choice(pool) for _ in range(2)]

    minions = []
    for key in minionKeys:
        baseDef = ENEMIES[key]
        scaled = dict(baseDef)
        scaled["level"] = baseDef.get("level", 1) + levelBonus
        if levelBonus > 0:
            scaled["base_hp"] = baseDef["base_hp"] + levelBonus * 5
            scaled["base_attack"] = baseDef["base_attack"] + levelBonus * 2
            scaled["base_defense"] = baseDef["base_defense"] + levelBonus
        minions.append(scaled)

    return [boss] + minions