"""
this file contains the definitions for Actions.
"""

from typing import Any, Dict

BASIC_ATTACK_DEF: Dict[str, Any] = {
    "key": "basic_strike",
    "name": "Strike",
    "description": "A direct physical blow relying solely on base damage.",
    "texture_id": "action_icons",
    "frame_index": 656,
    "scaling_stat": "attack",
    "multiplier": 1.0,
    "cooldown": 1,
    "grid_range": 1,
    "target_type": "enemy",  # "enemy", "ally", "self"
    "area_type": "single",   # "single", "cross", "square"
    "area_radius": 0,
    "effect": None,
    "is_basic": True,
}

# ---------------------
# UNIVERSAL ACTIONS

UNIVERSAL_ACTIONS: Dict[str, Dict[str, Any]] = {
    "slash": {
        "name": "Slash",
        "description": "Standard melee attack targeting an adjacent grid cell.",
        "texture_id": "action_icons",
        "frame_index": 720,  # icons since 720
        "scaling_stat": "attack",
        "multiplier": 1.3,
        "cooldown": 2,
        "grid_range": 1,
        "target_type": "enemy",
        "area_type": "single",
        "area_radius": 0,
        "effect": None,
        "is_basic": False,
    },
    "kick": {
        "name": "Kick",
        "description": "Search the weak point.",
        "texture_id": "action_icons",
        "frame_index": 720,  # icons since 720
        "scaling_stat": "agility",
        "multiplier": 1.3,
        "cooldown": 2,
        "grid_range": 1,
        "target_type": "enemy",
        "area_type": "single",
        "area_radius": 0,
        "effect": None,
        "is_basic": False,
    },
}

# ---------------------
# WARRIOR ACTIONS

WARRIOR_ACTIONS: Dict[str, Dict[str, Any]] = {
    "slam": {
        "name": "Slam",
        "description": "Heavy blunt bash that stuns the target on impact.",
        "texture_id": "action_icons", # Remember add the real name, ojopelao
        "frame_index": 858,
        "scaling_stat": "defense",
        "multiplier": 1.2,
        "cooldown": 4,
        "grid_range": 1,
        "target_type": "enemy",
        "area_type": "single",
        "area_radius": 1,
        "effect": "stun",
        "is_basic": False,
    },
    "fist": {
        "name": "Fist",
        "description": "In all the face.",
        "texture_id": "action_icons", # Remember add the real name, ojopelao
        "frame_index": 859,
        "scaling_stat": "attack",
        "multiplier": 1.2,
        "cooldown": 3,
        "grid_range": 1,
        "target_type": "enemy",
        "area_type": "single",
        "area_radius": 1,
        "effect": "stun",
        "is_basic": False,
    },
}

# ---------------------
# ROGUE ACTIONS

ROGUE_ACTIONS: Dict[str, Dict[str, Any]] = {
    "toxic_stab": {
        "name": "Toxic Stab",
        "description": "Swift piercing attack injecting lethal poison.",
        "texture_id": "action_icons",
        "frame_index": 729,
        "scaling_stat": "agility",
        "multiplier": 1.4,
        "cooldown": 3,
        "grid_range": 1,
        "target_type": "enemy",
        "area_type": "single",
        "area_radius": 1,
        "effect": "poison",
        "is_basic": False,
    },
    "toxic_slash": {
        "name": "Toxic Slash",
        "description": "Swift piercing attack injecting lethal poison.",
        "texture_id": "action_icons",
        "frame_index": 725,
        "scaling_stat": "agility",
        "multiplier": 1.2,
        "cooldown": 3,
        "grid_range": 2,
        "target_type": "enemy",
        "area_type": "single",
        "area_radius": 1,
        "effect": "poison",
        "is_basic": False,
    },
    "rain_daggers": {
        "name": "Rain of death",
        "description": "Spare a lot of daggers on a radius.",
        "texture_id": "action_icons",
        "frame_index": 736,
        "scaling_stat": "agility",
        "multiplier": 1.2,
        "cooldown": 3,
        "grid_range": 1,
        "target_type": "enemy",
        "area_type": "square",
        "area_radius": 1,
        "effect": "poison",
        "is_basic": False,
    },
    "rain_poison": {
        "name": "Rain of sick",
        "description": "Spare poison in a little radius.",
        "texture_id": "action_icons",
        "frame_index": 727,
        "scaling_stat": "agility",
        "multiplier": 1.2,
        "cooldown": 3,
        "grid_range": 2,
        "target_type": "enemy",
        "area_type": "square",
        "area_radius": 2,
        "effect": "poison",
        "is_basic": False,
    },
}

# ---------------------
# FAIRY ACTIONS

FAIRY_ACTIONS: Dict[str, Dict[str, Any]] = {
    "sparkle_heal": {
        "name": "Sparkle Heal",
        "description": "Restores health points to a targeted ally within range.",
        "texture_id": "action_icons",
        "frame_index": 776,  # Sparkles icon or heal
        "scaling_stat": "magic",
        "multiplier": 1.5,
        "cooldown": 3,
        "grid_range": 3,
        "target_type": "ally",
        "area_type": "single",
        "area_radius": 3,
        "effect": "heal",
        "is_basic": False,
    },
    "group_sanctuary": {
        "name": "Group Sanctuary",
        "description": "Radiates restorative fairy sparkles over an area.",
        "texture_id": "action_icons",
        "frame_index": 779,
        "scaling_stat": "magic",
        "multiplier": 1.1,
        "cooldown": 5,
        "grid_range": 2,
        "target_type": "ally",
        "area_type": "square",
        "area_radius": 1,
        "effect": "heal",
        "is_basic": False,
    },
    "sparkle_heal_self": {
        "name": "Sparkle Heal Self",
        "description": "Restores health points to a targeted ally within range.",
        "texture_id": "action_icons",
        "frame_index": 769,  # Sparkles icon or heal
        "scaling_stat": "magic",
        "multiplier": 1.5,
        "cooldown": 4,
        "grid_range": 1,
        "target_type": "self",
        "area_type": "single",
        "area_radius": 1,
        "effect": "heal",
        "is_basic": False,
    },
}

# ---------------------
# MAGE ACTIONS

MAGE_ACTIONS: Dict[str, Dict[str, Any]] = {
    "fireball": {
        "name": "Fireball",
        "description": "Casts a surging sphere of fire exploding into a zone.",
        "texture_id": "action_icons",
        "frame_index": 762,  # Fireball icon
        "scaling_stat": "magic",
        "multiplier": 1.6,
        "cooldown": 3,
        "grid_range": 3,
        "target_type": "enemy",
        "area_type": "cross",
        "area_radius": 1,
        "effect": None,
        "is_basic": False,
    },
    "frost_nova": {
        "name": "Frost Nova",
        "description": "Cast a powerful algo.",
        "texture_id": "action_icons",
        "frame_index": 785,
        "scaling_stat": "magic",
        "multiplier": 1.2,
        "cooldown": 4,
        "grid_range": 3,
        "target_type": "enemy",
        "area_type": "square",
        "area_radius": 1,
        "effect": None,
        "is_basic": False,
    },
    "hell_fire": {
        "name": "Hell Fire",
        "description": "Cast a powerful algo.",
        "texture_id": "action_icons",
        "frame_index": 758,
        "scaling_stat": "magic",
        "multiplier": 1.4,
        "cooldown": 4,
        "grid_range": 3,
        "target_type": "enemy",
        "area_type": "square",
        "area_radius": 3,
        "effect": None,
        "is_basic": False,
    },
}

# --------------------
# ENEMY ACTIONS

ENEMY_ACTIONS: Dict[str, Dict[str, Any]] = {
    "slime_acid": {
        "name": "Slime Acid",
        "description": "Splashes corrosive venom across adjacent targets.",
        "texture_id": "action_icons",
        "frame_index": 2,
        "scaling_stat": "attack",
        "multiplier": 0.9,
        "cooldown": 3,
        "grid_range": 1,
        "target_type": "enemy",
        "area_type": "single",
        "area_radius": 0,
        "effect": "poison",
        "is_basic": False,
    },
    "bone_toss": {
        "name": "Bone Toss",
        "description": "Hurls sharp bone fragments from a distance.",
        "texture_id": "action_icons",
        "frame_index": 1,
        "scaling_stat": "attack",
        "multiplier": 1.1,
        "cooldown": 3,
        "grid_range": 2,
        "target_type": "enemy",
        "area_type": "single",
        "area_radius": 0,
        "effect": None,
        "is_basic": False,
    },
    "dive": {
        "name": "Swoop Dive",
        "description": "Fast aerial charge staggering the target.",
        "texture_id": "action_icons",
        "frame_index": 1,
        "scaling_stat": "agility",
        "multiplier": 1.2,
        "cooldown": 3,
        "grid_range": 2,
        "target_type": "enemy",
        "area_type": "single",
        "area_radius": 0,
        "effect": "stun",
        "is_basic": False,
    },
    "hellfire_nova": {
        "name": "Hellfire Nova",
        "description": "Massive demonic burst covering an extensive area.",
        "texture_id": "action_icons",
        "frame_index": 4,
        "scaling_stat": "magic",
        "multiplier": 1.8,
        "cooldown": 3,
        "grid_range": 4,
        "target_type": "enemy",
        "area_type": "square",
        "area_radius": 2,
        "effect": "stun",
        "is_basic": False,
    },
}
