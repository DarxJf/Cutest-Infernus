from typing import Any, Dict

SCENERY: Dict[str, Dict[str, Any]] = {
    "rock": {
        "texture_id": "rock",
        "frame_index": 0,
        "is_solid": True,           
        "blocks_projectiles": True, 
    },
    "torch_red": {
        "texture_id": "floor_torch",
        "frame_index": 4,
        "is_solid": False,          
        "blocks_projectiles": False,
        "animation": [4, 5, 6, 7], 
        "animation_interval": 0.15,
    },
    "torch_green": {
        "texture_id": "floor_torch",
        "frame_index": 8,
        "is_solid": False,
        "blocks_projectiles": False,
        "animation": [8, 9, 10, 11],
        "animation_interval": 0.15,
    },
    "torch_blue": {
        "texture_id": "floor_torch",
        "frame_index": 12,
        "is_solid": False,
        "blocks_projectiles": False,
        "animation": [12, 13, 14, 15],
        "animation_interval": 0.15,
    },
    "torch_purple": {
        "texture_id": "floor_torch",
        "frame_index": 16,
        "is_solid": False,
        "blocks_projectiles": False,
        "animation": [16, 17, 18, 19],
        "animation_interval": 0.15,
    }
}