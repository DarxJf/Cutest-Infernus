"""
Module to define base physical of entities on the grid (board)
"""

from typing import Any, Dict, Optional
import pygame

from gale.state import StateMachine
from gale.animation import Animation

import settings

_DIRECTION_FALLBACK = {
    "left": "down",
    "right": "down",
}

class Entity():
    def __init__(self, definition: Dict[str, Any], x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y
        self.x = self.x * settings.TILE_SIZE
        self.y = self.y * settings.TILE_SIZE
        
        # Physical dimensions and rendering data
        self.width      = definition.get("width", settings.TILE_SIZE)
        self.height     = definition.get("height", settings.TILE_SIZE)
        self.textureId  = definition.get("texture")
        self.frameIndex = definition.get("frame_index", 0)
        
        # State and Animation management
        self.animations : Dict[str, Animation] = {}
        self.animationTextures: Dict[str, str] = {}

        self.currentAnimation: Optional[Animation] = None
        self.currentTextureId: Optional[str] = self.textureId
        self.state_machine = StateMachine()
        
        # Collision property
        self.isSolid = definition.get("is_solid", False)
        
        self._build_animation(definition.get("animations", {}))

    def _build_animation(self, animDefs:Dict [str, Dict[str, Any]]) -> None:
        for name, adef in animDefs.items():
            textureId = adef.get("texture", self.textureId)

            if textureId is None or textureId not in settings.FRAMES:

                continue

            frameList = settings.FRAMES[textureId]
            frames = [
                frameList[i]
                for i in adef.get("frames", [])
                if 0 <= i < len(frameList)
            ]

            if not frames:
                continue

            self.animations[name] = Animation(
                frames,
                adef.get("interval", 0),
                loops=adef.get("loops"),
            )
            self.animationTextures[name] = textureId

    def change_animation(self, name: str) -> None:
        resolved = self._resolve_animation_name(name)

        if resolved is None:
            return

        if self.currentAnimation is self.animations[resolved]:
            return

        self.currentAnimation = self.animations[resolved]
        self.currentTextureId = self.animationTextures[resolved]
        self.currentAnimation.reset()

    def _resolve_animation_name(self, name: str) -> Optional[str]:
        if name in self.animations:
            return name

        action, _, direction = name.partition("-")

        if direction in _DIRECTION_FALLBACK:
            fallbackName = f"{action}-{_DIRECTION_FALLBACK[direction]}"
            if fallbackName in self.animations:
                return fallbackName

        if action in self.animations:
            return action

        return None

    def update(self, dt: float)-> None:
        self.state_machine.update(dt)

        if self.currentAnimation is not None:
            self.currentAnimation.update(dt)


    def render(self, surface: pygame.Surface, offsetX, offsetY) -> None:
        if self.currentAnimation is not None and self.currentTextureId is not None:
            textureId = self.currentTextureId
            frame = self.currentAnimation.get_current_frame()
        else:
            if self.textureId is None or self.textureId not in settings.FRAMES:
                return
            textureId = self.textureId
            frame = settings.FRAMES[textureId][self.frameIndex]

        texture = settings.TEXTURES.get(textureId)

        if texture is None:
            return

        draw_x = self.x + (settings.TILE_SIZE - frame.width) // 2
        draw_y = self.y + (settings.TILE_SIZE - frame.height)

        surface.blit(texture, (draw_x + offsetX, draw_y + offsetY), frame)
