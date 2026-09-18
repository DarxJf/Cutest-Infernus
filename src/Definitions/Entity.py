"""
Definitions to entities on the board.
"""

from typing import Any, Dict


# ---------------------
# PLAYER CHARACTERS

PLAYER_CHARACTERS: Dict[str, Dict[str, Any]] = {
    "Cloud": {
        "name": "Cloud",
        "class_name": "Warrior",
        "texture": "cloud_walk",
        "width": 16, # Can change
        "height": 16, # Can change
        "frame_index": 0,
        "animations": {
            "idle-down": {
                "texture":"cloud_walk",
                "frames": [0, 1, 2,],
                "interval": 0.4
            },
            "idle-left": {
                "texture":"cloud_walk",
                "frames": [12, 13, 14,],
                "interval": 0.4
            },
            "idle-right": {
                "texture":"cloud_walk",
                "frames": [24, 25, 26,],
                "interval": 0.4
            },
            "idle-up": {
                "texture": "cloud_walk",
                "frames": [36, 37, 38,],
                "interval": 0.4
            },
            "walk-down": {
                "texture": "cloud_walk",
                "frames": [0, 1, 2,],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "cloud_walk",
                "frames": [12, 13, 14,],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "cloud_walk",
                "frames": [24, 25, 26,],
                "interval": 0.15
            },
            "walk-up":{
                "texture": "cloud_walk",
                "frames": [36, 37, 38,],
                "interval": 0.15
            },
            "attack-down": {
                "texture": "cloud_walk",
                "frames": [0, 1, 2,],
                "interval": 0.15
            },
            "attack-left": {
                "texture": "cloud_walk",
                "frames": [12, 13, 14,],
                "interval": 0.15
            },
            "attack-right": {
                "texture": "cloud_walk",
                "frames": [24, 25, 26,],
                "interval": 0.15
            },
            "attack-up":{
                "texture": "cloud_walk",
                "frames": [36, 37, 38,],
                "interval": 0.15
            },
        },
        "base_hp": 35,
        "base_attack": 9,
        "base_magic": 4,
        "base_agility": 4,
        "base_defense": 10,
        "base_magic_defense": 6,
        "basic_attack": "strike",
        "base_rest": 3.0,
        "base_movement": 3,
        "default_actions": ["slash", "slam", "ground_smash"],
        "slot_actions": 4,
        "slot_objects": 1,
        "role": "main",
    },
    "Pelusa": {
        "name": "Pelusa",
        "class_name": "Rogue",
        "texture": "pelusa_walk",
        "width": 16,
        "height": 16,
        "frame_index": 0,
        "animations": {
            "idle-down": {
                "texture": "pelusa_walk",
                "frames": [0, 1, 2, 4,],
                "interval": 0.4
            },
            "idle-left": {
                "texture": "pelusa_walk",
                "frames": [12, 13, 14, 4,],
                "interval": 0.4
            },
            "idle-right": {
                "texture": "pelusa_walk",
                "frames": [24, 25, 26, 4,],
                "interval": 0.4
            },
            "idle-up": {
                "texture": "pelusa_walk",
                "frames": [36, 37, 38, 4, 5],
                "interval": 0.4
            },
            "walk-down": {
                "texture": "pelusa_walk",
                "frames": [0, 1, 2,],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "pelusa_walk",
                "frames": [12, 13, 14,],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "pelusa_walk",
                "frames": [24, 25, 26,],
                "interval": 0.15
            },
            "walk-up": {
                "texture": "pelusa_walk",
                "frames": [36, 37, 38,],
                "interval": 0.15
            },
            "attack-down": {
                "texture": "pelusa_walk",
                "frames": [0, 1, 2,],
                "interval": 0.15
            },
            "attack-left": {
                "texture": "pelusa_walk",
                "frames": [12, 13, 14,],
                "interval": 0.15
            },
            "attack-right": {
                "texture": "pelusa_walk",
                "frames": [24, 25, 26,],
                "interval": 0.15
            },
            "attack-up": {
                "texture": "pelusa_walk",
                "frames": [36, 37, 38,],
                "interval": 0.15
            },
        },
        "base_hp": 28,
        "base_attack": 7,
        "base_magic": 3,
        "base_agility": 10,
        "base_defense": 4,
        "base_magic_defense": 4,
        "basic_attack": "strike",
        "base_rest": 2.0,
        "base_movement": 4,
        "default_actions": ["slash", "toxic_stab"],
        "slot_actions": 4,
        "slot_objects": 1,
        "role": "main",
    },
    "Chloe": {
        "name": "Chloe",
        "class_name": "Fairy",
        "texture": "chloe_walk",
        "width": 16,
        "height": 16,
        "frame_index": 0,
        "animations": {
            "idle-down": {
                "texture": "chloe_walk",
                "frames": [0, 1, 2,],
                "interval": 0.4
            },
            "idle-left": {
                "texture": "chloe_walk",
                "frames": [12, 13, 14,],
                "interval": 0.4
            },
            "idle-right": {
                "texture": "chloe_walk",
                "frames": [24, 25, 26,],
                "interval": 0.4
            },
            "idle-up": {
                "texture": "chloe_walk",
                "frames": [36, 37, 38,],
                "interval": 0.4
            },
            "walk-down": {
                "texture": "chloe_walk",
                "frames": [0, 1, 2,],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "chloe_walk",
                "frames": [12, 13, 14,],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "chloe_walk",
                "frames": [24, 25, 26,],
                "interval": 0.15
            },
            "walk-up": {
                "texture": "chloe_walk",
                "frames": [36, 37, 38,],
                "interval": 0.15
            },
            "attack-down": {
                "texture": "chloe_walk",
                "frames": [0, 1, 2,],
                "interval": 0.15
            },
            "attack-left": {
                "texture": "chloe_walk",
                "frames": [12, 13, 14,],
                "interval": 0.15
            },
            "attack-right": {
                "texture": "chloe_walk",
                "frames": [24, 25, 26,],
                "interval": 0.15
            },
            "attack-up": {
                "texture": "chloe_walk",
                "frames": [36, 37, 38,],
                "interval": 0.15
            },
        },
        "base_hp": 24,
        "base_attack": 6,
        "base_magic": 9,
        "base_agility": 6,
        "base_defense": 4,
        "base_magic_defense": 8,
        "basic_attack": "strike",
        "base_rest": 2.5,
        "base_movement": 3,
        "default_actions": ["slash", "sparkle_heal", "fairy_bolt", "sparkle_heal_self"],
        "slot_actions": 4,
        "slot_objects": 1,
        "role": "main",
    },
    "Balthazar": {
        "name": "Balthazar",
        "class_name": "Mage",
        "texture": "balthazar_walk",
        "width": 16,
        "height": 16,
        "frame_index": 0,
        "animations": {
            "idle-down": {
                "texture": "balthazar_walk",
                "frames": [0, 1, 2, 3, 16, 17,],
                "interval": 0.4
            },
            "idle-left": {
                "texture": "balthazar_walk",
                "frames": [12, 13, 14, 3, 16, 17,],
                "interval": 0.4
            },
            "idle-right": {
                "texture": "balthazar_walk",
                "frames": [24, 25, 26, 3, 16, 17,],
                "interval": 0.4
            },
            "idle-up": {
                "texture": "balthazar_walk",
                "frames": [36, 37, 38, 3, 16, 17,],
                "interval": 0.4
            },
            "walk-down": {
                "texture": "balthazar_walk",
                "frames": [0, 1, 2,],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "balthazar_walk",
                "frames": [12, 13, 14,],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "balthazar_walk",
                "frames": [24, 25, 26,],
                "interval": 0.15
            },
            "walk-up": {
                "texture": "balthazar_walk",
                "frames": [36, 37, 38,],
                "interval": 0.15
            },
            "attack-down": {
                "texture": "balthazar_walk",
                "frames": [0, 1, 2, 15,],
                "interval": 0.15
            },
            "attack-left": {
                "texture": "balthazar_walk",
                "frames": [12, 13, 14, 15,],
                "interval": 0.15
            },
            "attack-right": {
                "texture": "balthazar_walk",
                "frames": [24, 25, 26, 15,],
                "interval": 0.15
            },
            "attack-up": {
                "texture": "balthazar_walk",
                "frames": [36, 37, 38,],
                "interval": 0.15
            },
        },
        "base_hp": 22,
        "base_attack": 4,
        "base_magic": 10,
        "base_agility": 5,
        "base_defense": 3,
        "base_magic_defense": 3,
        "basic_attack": "strike",
        "base_rest": 3.0,
        "base_movement": 2,
        "default_actions": ["slash", "fireball", "frost_nova"],
        "slot_actions": 5,
        "slot_objects": 2,
        "role": "main", 
    },


    # ---------------------
    # SECONDARY CHARACTERS
    # ---------------------

    # --- Warriors ---
    "Siegfried": {
        "name": "Siegfried",
        "class_name": "Warrior",
        "texture": "cloud_walk",        
        "width": 16,
        "height": 16,
        "frame_index": 48,
        "animations": {
            "idle-down": {
                "texture":"cloud_walk",
                "frames": [48, 49, 50,],
                "interval": 0.2
            },
            "idle-left": {
                "texture":"cloud_walk",
                "frames": [60, 61, 62,],
                "interval": 0.2
            },
            "idle-right": {
                "texture":"cloud_walk",
                "frames": [72, 73, 74,],
                "interval": 0.2
            },
            "idle-up": {
                "texture": "cloud_walk",
                "frames": [84, 85, 86,],
                "interval": 0.2
            },
            "walk-down": {
                "texture": "cloud_walk",
                "frames": [48, 49, 50,],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "cloud_walk",
                "frames": [60, 61, 62,],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "cloud_walk",
                "frames": [72, 73, 74,],
                "interval": 0.15
            },
            "walk-up":{
                "texture": "cloud_walk",
                "frames": [84, 85, 86,],
                "interval": 0.15
            },
            "attack-down": {
                "texture": "cloud_walk",
                "frames": [48, 49, 50,],
                "interval": 0.15
            },
            "attack-left": {
                "texture": "cloud_walk",
                "frames": [60, 61, 62,],
                "interval": 0.15
            },
            "attack-right": {
                "texture": "cloud_walk",
                "frames": [72, 73, 74,],
                "interval": 0.15
            },
            "attack-up":{
                "texture": "cloud_walk",
                "frames": [84, 85, 86,],
                "interval": 0.15
            },
        },
        "base_hp": 30,
        "base_attack": 9,
        "base_magic": 1,
        "base_agility": 2,
        "base_defense": 8,
        "base_magic_defense": 5,
        "basic_attack": "strike",
        "base_rest": 3.5,
        "base_movement": 3,
        "default_actions": ["slash", "slam"],
        "slot_actions": 4,
        "slot_objects": 1,
        "role": "secondary",
    },
     # --- Rogues ---
    "Raven": {
        "name": "Raven",
        "class_name": "Rogue",
        "texture": "pelusa_walk",
        "width": 16,
        "height": 16,
        "frame_index": 48,
        "animations": {
            "idle-down": {
                "texture": "pelusa_walk",
                "frames": [48, 49, 50,],
                "interval": 0.2
            },
            "idle-left": {
                "texture": "pelusa_walk",
                "frames": [60, 61, 62,],
                "interval": 0.2
            },
            "idle-right": {
                "texture": "pelusa_walk",
                "frames": [72, 73, 74,],
                "interval": 0.2
            },
            "idle-up": {
                "texture": "pelusa_walk",
                "frames": [84, 85, 86,],
                "interval": 0.2
            },
            "walk-down": {
                "texture": "pelusa_walk",
                "frames": [48, 49, 50,],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "pelusa_walk",
                "frames": [60, 61, 62,],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "pelusa_walk",
                "frames": [72, 73, 74,],
                "interval": 0.15
            },
            "walk-up": {
                "texture": "pelusa_walk",
                "frames": [84, 85, 86,],
                "interval": 0.15
            },
            "attack-down": {
                "texture": "pelusa_walk",
                "frames": [48, 49, 50,],
                "interval": 0.15
            },
            "attack-left": {
                "texture": "pelusa_walk",
                "frames": [60, 61, 62,],
                "interval": 0.15
            },
            "attack-right": {
                "texture": "pelusa_walk",
                "frames": [72, 73, 74,],
                "interval": 0.15
            },
            "attack-up": {
                "texture": "pelusa_walk",
                "frames": [84, 85, 86,],
                "interval": 0.15
            },
        },
        "base_hp": 22,
        "base_attack": 6,
        "base_magic": 5,
        "base_agility": 8,
        "base_defense": 3,
        "base_magic_defense": 3,
        "basic_attack": "strike",
        "base_rest": 1.8,
        "base_movement": 4,
        "default_actions": ["slash", "toxic_stab"],
        "slot_actions": 4,
        "slot_objects": 1,
        "role": "secondary",
    },
    "Lumina": {
        "name": "Lumina",
        "class_name": "Fairy",
        "texture": "chloe_walk",
        "width": 16,
        "height": 16,
        "frame_index": 48,
        "animations": {
            "idle-down": {
                "texture": "chloe_walk",
                "frames": [48, 49, 50,],
                "interval": 0.2
            },
            "idle-left": {
                "texture": "chloe_walk",
                "frames": [60, 61, 62,],
                "interval": 0.2
            },
            "idle-right": {
                "texture": "chloe_walk",
                "frames": [72, 73, 74,],
                "interval": 0.2
            },
            "idle-up": {
                "texture": "chloe_walk",
                "frames": [84, 85, 86,],
                "interval": 0.2
            },
            "walk-down": {
                "texture": "chloe_walk",
                "frames": [48, 49, 50,],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "chloe_walk",
                "frames": [60, 61, 62,],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "chloe_walk",
                "frames": [72, 73, 74,],
                "interval": 0.15
            },
            "walk-up": {
                "texture": "chloe_walk",
                "frames": [84, 85, 86,],
                "interval": 0.15
            },
            "attack-down": {
                "texture": "chloe_walk",
                "frames": [48, 49, 50,],
                "interval": 0.15
            },
            "attack-left": {
                "texture": "chloe_walk",
                "frames": [60, 61, 62,],
                "interval": 0.15
            },
            "attack-right": {
                "texture": "chloe_walk",
                "frames": [72, 73, 74,],
                "interval": 0.15
            },
            "attack-up": {
                "texture": "chloe_walk",
                "frames": [84, 85, 86,],
                "interval": 0.15
            },
        },
        "base_hp": 22,
        "base_attack": 3,
        "base_magic": 8,
        "base_agility": 6,
        "base_defense": 3,
        "base_magic_defense": 6,
        "basic_attack": "strike",
        "base_rest": 2.5,
        "base_movement": 3,
        "default_actions": ["sparkle_heal", "group_sanctuary"],
        "slot_actions": 4,
        "slot_objects": 1,
        "role": "secondary",
    },
    "Alistair": {
        "name": "Alistair",
        "class_name": "Mage",
        "texture": "balthazar_walk",
        "width": 16,
        "height": 16,
        "frame_index": 48,
        "animations": {
            "idle-down": {
                "texture": "balthazar_walk",
                "frames": [48, 49, 50,],
                "interval": 0.2
            },
            "idle-left": {
                "texture": "balthazar_walk",
                "frames": [60, 61, 62,],
                "interval": 0.2
            },
            "idle-right": {
                "texture": "balthazar_walk",
                "frames": [72, 73, 74,],
                "interval": 0.2
            },
            "idle-up": {
                "texture": "balthazar_walk",
                "frames": [84, 85, 86,],
                "interval": 0.2
            },
            "walk-down": {
                "texture": "balthazar_walk",
                "frames": [48, 49, 50,],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "balthazar_walk",
                "frames": [60, 61, 62,],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "balthazar_walk",
                "frames": [72, 73, 74,],
                "interval": 0.15
            },
            "walk-up": {
                "texture": "balthazar_walk",
                "frames": [84, 85, 86,],
                "interval": 0.15
            },
            "attack-down": {
                "texture": "balthazar_walk",
                "frames": [48, 49, 50,],
                "interval": 0.15
            },
            "attack-left": {
                "texture": "balthazar_walk",
                "frames": [60, 61, 62,],
                "interval": 0.15
            },
            "attack-right": {
                "texture": "balthazar_walk",
                "frames": [72, 73, 74,],
                "interval": 0.15
            },
            "attack-up": {
                "texture": "balthazar_walk",
                "frames": [84, 85, 86,],
                "interval": 0.15
            },
        },
        "base_hp": 26,
        "base_attack": 5,
        "base_magic": 9,
        "base_agility": 4,
        "base_defense": 4,
        "base_magic_defense": 5,
        "basic_attack": "strike",
        "base_rest": 2.8,
        "base_movement": 2,
        "default_actions": ["fireball",],
        "slot_actions": 5,
        "slot_objects": 2,
        "role": "secondary",
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
        "base_hp": 18,
        "base_attack": 8,
        "base_magic": 2,
        "base_agility": 2,
        "base_defense": 7,
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
        "base_hp": 34,
        "base_attack": 9,
        "base_magic": 1,
        "base_agility": 4,
        "base_defense": 8,
        "base_magic_defense": 4,
        "basic_attack": "strike",
        "base_rest": 2.8,
        "base_movement": 3,
        "default_actions": ["bone_toss", "death_call"],
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
        "base_hp": 50,
        "base_attack": 10,
        "base_magic": 9,
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
    "boss": {
        "class_name": "Boss",
        "name": "Soul Devourer",
        "width": 32,
        "height": 32,
        "frame_index": 0,
        "animations": {
            "idle-down": {
                "texture":"boss-idle",
                "frames": [0, 1, 2, 3],
                "interval": 0.2
            },
            "idle-left": {
                "texture":"boss-idle",
                "frames": [12, 13, 14, 15],
                "interval": 0.2
            },
            "idle-right": {
                "texture":"boss-idle",
                "frames": [4, 5, 6, 7],
                "interval": 0.2
            },
            "idle-up": {
                "texture": "boss-idle",
                "frames": [8, 9, 10, 11],
                "interval": 0.2
            },
            "walk-down": {
                "texture": "boss-walk",
                "frames": [0, 1, 2, 3],
                "interval": 0.15
            },
            "walk-left": {
                "texture": "boss-walk",
                "frames": [12, 13, 14, 15],
                "interval": 0.15
            },
            "walk-right": {
                "texture": "boss-walk",
                "frames": [4, 5, 6, 7],
                "interval": 0.15
            },
            "walk-up":{
                "texture": "boss-walk",
                "frames": [8, 9, 10, 11],
                "interval": 0.15
            }
        },
        "base_hp": 70,
        "base_attack": 12,
        "base_magic": 12,
        "base_agility": 12,
        "base_defense": 12,
        "base_magic_defense": 12,
        "basic_attack": "strike",
        "base_rest": 4.0,
        "base_movement": 3,
        "default_actions": ["dive", "hellfire_nova", "death_call"],
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
    "Warrior": {"hp": 5, "attack": 4, "magic": 1, "agility": 3, "defense": 4, "magic_defense": 4},
    "Rogue":   {"hp": 5, "attack": 2, "magic": 1, "agility": 5, "defense": 1, "magic_defense": 2},
    "Fairy":   {"hp": 5, "attack": 2, "magic": 4, "agility": 2, "defense": 3, "magic_defense": 3},
    "Mage":    {"hp": 5, "attack": 1, "magic": 5, "agility": 2, "defense": 1, "magic_defense": 3},
}

def get_main_characters() -> Dict[str, Dict[str, Any]]:
    """Characters the player picks from at the start of a run."""
    return {k: v for k, v in PLAYER_CHARACTERS.items() if v.get("role") == "main"}


def get_secondary_characters() -> Dict[str, Dict[str, Any]]:
    """Recruitable NPCs that appear in the rest area."""
    return {k: v for k, v in PLAYER_CHARACTERS.items() if v.get("role") == "secondary"}

def get_character_by_key(key: str) -> Dict[str, Any]:
    if key not in PLAYER_CHARACTERS:
        raise KeyError(f"Unknown character key: {key!r}")
    return PLAYER_CHARACTERS[key]
