"""Module containing the definitions for equipable passive objects."""

from typing import Any, Dict

# ----------------
# OBJECTS DEFINITIONS

PASSIVE_OBJECTS: Dict[str, Dict[str, Any]] = {
    "vitality_ring": {
        "name": "Ring of Vitality",
        "description": "A crimson ring that increases maximum health and slight defense.",
        "texture_id": "object_icons",
        "frame_index": 42,
        "stat_modifiers": {
            "hp": 15,
            "defense": 2
        }
    },
    "sage_necklace": {
        "name": "Sage's Necklace",
        "description": "An ancient necklace pulsing with magical energy.",
        "texture_id": "object_icons",
        "frame_index": 32,
        "stat_modifiers": {
            "magic": 8,
            "magic_defense": 4
        }
    },
    "brute_belt": {
        "name": "Brute's Belt",
        "description": "A heavy belt that empowers physical strikes but reduces speed.",
        "texture_id": "object_icons",
        "frame_index": 55,
        "stat_modifiers": {
            "attack": 6,
            "agility": -2  # Los objetos también pueden tener efectos negativos
        }
    },
    "swift_boots": {
        "name": "Swift Boots",
        "description": "Lightweight boots that greatly increase agility and rest recovery.",
        "texture_id": "object_icons",
        "frame_index": 57,
        "stat_modifiers": {
            "agility": 5,
            "rest": -0.5  # Reduce el tiempo base de descanso
        }
    },
    "iron_sword": {
        "name": "Iron Sword",
        "description": "A sturdy blade for frontline fighters.",
        "texture_id": "action_icons",
        "frame_index": 1735,
        "stat_modifiers": {"attack": 4},
    },
    "assassin_dagger": {
        "name": "Assassin's Dagger",
        "description": "Sharp and quick, but fragile.",
        "texture_id":  "action_icons",
        "frame_index": 1685,
        "stat_modifiers": {
            "attack": 8,
            "defense": -3
        },
    },
    "iron_shield": {
        "name": "Iron Shield",
        "description": "Heavy protection for those who can bear it.",
        "texture_id":  "action_icons",
        "frame_index": 1810,
        "stat_modifiers": {
            "defense": 5,
            "agility": -2
        },
    },
    "guardian_plate": {
        "name": "Guardian Plate",
        "description": "A blessed plate that bolsters body and mind.",
        "texture_id":  "action_icons",
        "frame_index": 2139,
        "stat_modifiers": {
            "defense": 6,
            "magic_defense": 6
        },
    },
    "arcane_orb": {
        "name": "Arcane Orb",
        "description": "A humming sphere of pure mana.",
        "texture_id":  "action_icons",
        "frame_index": 169,
        "stat_modifiers": {"magic": 6},
    },
    "warlock_tome": {
        "name": "Warlock's Tome",
        "description": "Forbidden knowledge, at a cost.",
        "texture_id":  "action_icons",
        "frame_index": 103,
        "stat_modifiers": {
            "magic": 10,
            "hp": -10
        },
    },
    "swift_charm": {
        "name": "Swift Charm",
        "description": "A tiny charm that quickens the wearer.",
        "texture_id": "action_icons",
        "frame_index": 691,
        "stat_modifiers": {"agility": 6},
    },
    "wind_cloak": {
        "name": "Wind Cloak",
        "description": "Woven from the breath of storms.",
        "texture_id":  "action_icons",
        "frame_index": 2029,
        "stat_modifiers": {
            "agility": 10,
            "defense": -3},
    },
    "hero_medal": {
        "name": "Hero's Medal",
        "description": "A symbol of courage, granting many small blessings.",
        "texture_id":  "action_icons",
        "frame_index": 2178,
        "stat_modifiers": {
            "attack": 3,
            "defense": 3,
            "magic": 3,
            "agility": 3
        },
    },
    "cursed_ring": {
        "name": "Cursed Ring",
        "description": "Power at a price.",
        "texture_id":  "action_icons",
        "frame_index": 2184,
        "stat_modifiers": {
            "attack": 12,
            "defense": -4,
            "magic_defense": -4
        },
    },

}