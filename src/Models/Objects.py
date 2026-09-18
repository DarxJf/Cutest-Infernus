"""Module defining the PassiveObject class for the equipment slot."""

from typing import Any, Dict
import pygame

import settings

class PassiveObject:
    def __init__(self, key: str, definition: Dict[str, Any]) -> None:
        self.key = key
        
        # Defensive programming to safely extract strings and sprites
        self.name = definition.get("name", "Unknown Object")
        self.description = definition.get("description", "No description available.")
        self.textureId = definition.get("texture_id")
        self.frameIndex = definition.get("frame_index", 0)
        
        # The "effect" is safely extracted as a dictionary
        self.statModifiers = definition.get("stat_modifiers", {})

    def render(self, surface: pygame.Surface, x: float, y: float) -> None:
        # if self.textureId in settings.TEXTURES:
        #     frame = settings.FRAMES[self.textureId][self.frameIndex]
        #     surface.blit(settings.TEXTURES[self.textureId], (x, y), frame)
        pass

    def equip_object(self, entity: Any) -> None:
        for stat, modifier in self.statModifiers.items():
            if hasattr(entity, stat):
                current_value = getattr(entity, stat)
                setattr(entity, stat, current_value + modifier)
        if "hp" in self.statModifiers and hasattr(entity, "currentHp"):
            entity.currentHp = min(entity.currentHp, entity.hp)

    def unequip_object(self, entity: Any) -> None:
        for stat, modifier in self.statModifiers.items():
            if hasattr(entity, stat):
                current_value = getattr(entity, stat)
                setattr(entity, stat, current_value - modifier)
        if "hp" in self.statModifiers and hasattr(entity, "currentHp"):
            entity.currentHp = min(entity.currentHp, entity.hp)