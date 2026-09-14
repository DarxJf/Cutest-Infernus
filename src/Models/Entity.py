"""
Module to define base physical of entities on the grid (board)
"""

from typing import Any, Dict
import pygame

# from gale.state import StateMachine

import settings


class Entity():
    def __init__(self, definition: Dict[str, Any], x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y
        
        # Physical dimensions and rendering data
        self.width      = definition.get("width", 16)
        self.height     = definition.get("height", 16)
        self.textureId  = definition.get("texture")
        self.frameIndex = definition.get("frame_index", 0)
        
        # State and Animation management
        self.animations = definition.get("animations", {})
        self.currentAnimation = None
        # self.state_machine = StateMachine()
        
        # Collision property
        self.isSolid = definition.get("is_solid", False)
        
        # Pixel coordinates (assuming a 16x16 grid tile size) could change
        self.x = self.x * 16
        self.y = self.y * 16

    def change_state(self, state_name: str, *args: Any) -> None:
        # self.state_machine.change(state_name, *args)
        pass

    def change_animation(self, animation_name: str) -> None:
        if animation_name in self.animations:
            self.current_animation = self.animations[animation_name]

    def update(self, dt: float) -> None:
        # self.state_machine.update(dt)
        if self.currentAnimation:
            self.currentAnimation.update(dt)

    def render(self, surface: pygame.Surface, offsetX, offsetY) -> None:
        if self.textureId in settings.TEXTURES:
            if self.currentAnimation:
                frame = self.currentAnimation.get_current_frame()
            else:
                frame = settings.FRAMES[self.textureId][self.frameIndex]

        draw_x = self.x + (settings.TILE_SIZE - frame.width) // 2
        draw_y = self.y + (settings.TILE_SIZE - frame.height)
        
        # 3. Dibujamos sumando el desfase de la cámara (Room)
        surface.blit(
            settings.TEXTURES[self.textureId], 
            (draw_x + offsetX, draw_y + offsetY), 
            frame
        )
