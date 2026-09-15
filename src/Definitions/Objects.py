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
    }
}