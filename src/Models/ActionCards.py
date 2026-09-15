from typing import Any, Dict
import pygame

import settings

class Action:
    def __init__(self, key: str, definition: Dict[str, Any]) -> None:
        self.key = key
        self.name        = definition["name"]
        self.description = definition["description"]
        self.textureId   = definition["texture_id"]
        self.frameIndex  = definition["frame_index"]
        self.scalingStat = definition["scaling_stat"]
        self.multiplier  = definition["multiplier"]
        self.cooldown    = definition["cooldown"]
        self.gridRange   = definition["grid_range"]
        self.targetType  = definition["target_type"]  # "enemy", "ally", "self"
        self.areaType    = definition["area_type"]      # "single", "cross", "square"
        self.areaRadius  = definition["area_radius"]
        self.effect      = definition.get("effect")       # "stun", "poison", "heal", None
        self.isBasic     = definition.get("is_basic", False)

    # def render(self, surface: pygame.Surface, x: float, y: float) -> None:
    #     """Renders the action icon for UI menus using Gale frames and Pygame."""
    #     if self.textureId in settings.TEXTURES:
    #         frame = settings.FRAMES[self.textureId][self.frameIndex]
    #         surface.blit(settings.TEXTURES[self.textureId], (x, y), frame)