"""
Definitions to entities on the board.
"""

from typing import Any, Dict


# ---------------------
# PLAYER CHARACTERS

PLAYER_CHARACTERS: Dict[str, Dict[str, Any]] = {
    "Cloud": {
        "class_name": "Warrior",
        "texture": "cloud_walk",
        "width": 16, # Can change
        "height": 16, # Can change
        "frame_index": 13,
        "animations": {
            # idle: [0]
            # walk: [0, 1, 2, 3]
        },
        "base_hp": 40,
        "base_attack": 14,
        "base_magic": 2,
        "base_agility": 4,
        "base_defense": 10,
        "base_magic_defense": 3,
        "basic_attack": "strike",
        "base_rest": 3.0,
        "base_movement": 3,
        "default_actions": ["slash", "slam"],
        "slot_actions": 4,
        "slot_objects": 1,
    },
    "Pelusa": {
        "class_name": "Rogue",
        "texture": "pelusa_walk",
        "width": 16,
        "height": 16,
        "frame_index": 0,
        "animations": {},
        "base_hp": 28,
        "base_attack": 11,
        "base_magic": 3,
        "base_agility": 10,
        "base_defense": 6,
        "base_magic_defense": 5,
        "basic_attack": "strike",
        "base_rest": 2.0,
        "base_movement": 3,
        "default_actions": ["slash", "toxic_stab"],
        "slot_actions": 4,
        "slot_objects": 1,
    },
    "Chloe": {
        "class_name": "Fairy",
        "texture": "chloe_walk",
        "width": 16,
        "height": 16,
        "frame_index": 0,
        "animations": {},
        "base_hp": 24,
        "base_attack": 5,
        "base_magic": 14,
        "base_agility": 7,
        "base_defense": 4,
        "base_magic_defense": 10,
        "basic_attack": "strike",
        "base_rest": 2.5,
        "base_movement": 3,
        "default_actions": ["slash", "sparkle_heal", "group_sanctuary"],
        "slot_actions": 4,
        "slot_objects": 1,
    },
    "Balthazar": {
        "class_name": "Mage",
        "texture": "balthazar_walk",
        "width": 16,
        "height": 16,
        "frame_index": 0,
        "animations": {},
        "base_hp": 22,
        "base_attack": 4,
        "base_magic": 16,
        "base_agility": 5,
        "base_defense": 3,
        "base_magic_defense": 11,
        "basic_attack": "strike",
        "base_rest": 3.0,
        "base_movement": 3,
        "default_actions": ["slash", "fireball"],
        "slot_actions": 5,
        "slot_objects": 1,
    },
}

# ---------------------
# ENEMIES

ENEMIES: Dict[str, Dict[str, Any]] = {
	"slime": {
        "class_name": "Slime",
        "width": 16,
        "height": 17,
        "frame_index": 0,
        "animations": {
            "idle-down": {
                "texture": "slime-down",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.2
            },
            "idle-up": {
                "texture": "slime-up",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.2
            },
            "walk-down": {
                "texture": "slime-down",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            },
            "walk-up":{
                "texture": "slime-up",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            }
        },
        "base_hp": 20,
        "base_attack": 8,
        "base_magic": 2,
        "base_agility": 2,
        "base_defense": 5,
        "base_magic_defense": 2,
        "basic_attack": "strike",
        "base_rest": 3.0,
        "base_movement": 3,
        "default_actions": ["slime_acid"],
        "soul_value": 10,
        "exp_value": 15,
    },
    "skeleton": {
        "class_name": "Skeleton",
        "width": 16,
        "height": 17,
        "frame_index": 0,
       "animations": {
            "idle-down": {
                "texture":"skel-idle-down" ,
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.2
            },
            "idle-left": {
                "texture":"skel-idle-left" ,
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.2
            },
            "idle-right": {
                "texture":"skel-idle-right" ,
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.2
            },
            "idle-up": {
            "texture": "skel-idle-up",
            "frames": [0, 1, 2, 3, 4, 5],
            "interval": 0.2
            },
            "walk-down": {
                "texture": "skel-walk-down",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "skel-walk-left",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "skel-walk-right",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            },
            "walk-up":{
                "texture": "skel-walk-up",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            }
        },
        "base_hp": 26,
        "base_attack": 10,
        "base_magic": 1,
        "base_agility": 4,
        "base_defense": 8,
        "base_magic_defense": 2,
        "basic_attack": "strike",
        "base_rest": 2.8,
        "base_movement": 3,
        "default_actions": ["bone_toss"],
        "soul_value": 15,
        "exp_value": 20,
    },
    "demon": {
        "class_name": "Demon",
        "width": 16,
        "height": 17,
        "frame_index": 0,
        "animations": {
            "idle-down": {
                "texture":"demon-idle-down" ,
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.2
            },
            "idle-left": {
                "texture":"demon-idle-left" ,
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.2
            },
            "idle-right": {
                "texture":"demon-idle-right" ,
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.2
            },
            "idle-up": {
                "texture": "demon-idle-up",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.2
            },
            "walk-down": {
                "texture": "demon-walk-down",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "demon-walk-left",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "demon-walk-right",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            },
            "walk-up":{
                "texture": "demon-walk-up",
                "frames": [0, 1, 2, 3, 4, 5],
                "interval": 0.15
            }
        },
        "base_hp": 60,
        "base_attack": 15,
        "base_magic": 12,
        "base_agility": 6,
        "base_defense": 10,
        "base_magic_defense": 9,
        "basic_attack": "strike",
        "base_rest": 4.0,
        "base_movement": 3,
        "default_actions": ["dive", "hellfire_nova"],
        "soul_value": 40,
        "exp_value": 60,
    },
}

# ---------------------
# SOLID OBJECTS

SOLID_OBJECTS: Dict[str, Dict[str, Any]] = {
	"rock": {
		"texture": "world_objects",
		"width": 16,
		"height": 16,
		"frame_index": 0,
		"is_solid": True,
		"animations": {},
	},
}

# -------------
# CLASSES DEFINITIONS

CLASS_MODIFIERS: Dict[str, Dict[str, Any]] = {
    "Warrior": {
        "stat_multipliers": {
            "base_attack": 1.35,
            "base_defense": 1.30,
            "base_magic_defense": 1.15,
            "base_magic": 0.60,
            "base_agility": 0.75,
        },
        "bonus_action_slots": 0,
        "bonus_object_slots": 0,
    },
    "Rogue": {
        "stat_multipliers": {
            "base_attack": 1.50,
            "base_defense": 0.70,
            "base_magic_defense": 0.70,
            "base_agility": 1.40,
            "base_magic": 1.00,
        },
        "bonus_action_slots": 0,
        "bonus_object_slots": 0,
    },
    "Fairy": {
        "stat_multipliers": {
            "base_magic": 1.40,
            "base_magic_defense": 1.35,
            "base_attack": 0.50,
            "base_defense": 0.60,
            "base_agility": 1.10,
        },
        "bonus_action_slots": 0,
        "bonus_object_slots": 0,
    },
    "Mage": {
        "stat_multipliers": {
            "base_magic": 1.60,
            "base_attack": 0.80,
            "base_defense": 0.80,
            "base_magic_defense": 1.10,
            "base_agility": 0.90,
        },
        "bonus_action_slots": 1,
        "bonus_object_slots": 1,
    },
}

LEVEL_GROWTH: Dict[str, Dict[str, int]] = {
    "Warrior": {"hp": 5, "attack": 2, "magic": 0, "agility": 0, "defense": 2, "magic_defense": 1},
    "Rogue":   {"hp": 3, "attack": 2, "magic": 0, "agility": 3, "defense": 1, "magic_defense": 1},
    "Fairy":   {"hp": 2, "attack": 0, "magic": 4, "agility": 1, "defense": 0, "magic_defense": 2},
    "Mage":    {"hp": 2, "attack": 0, "magic": 5, "agility": 1, "defense": 0, "magic_defense": 2},
}
