"""Small helpers to fetch icon surfaces from a spritesheet frame list."""

from typing import Optional

import pygame

import settings


def icon_surface(textureId: str, frameIndex: int) -> Optional[pygame.Surface]:
    """
    Returns a standalone Surface for one frame of a spritesheet, so it
    can be blitted anywhere without carrying the parent texture around.
    """
    if textureId not in settings.TEXTURES or textureId not in settings.FRAMES:
        return None

    frames = settings.FRAMES[textureId]
    if not (0 <= frameIndex < len(frames)):
        return None

    rect = frames[frameIndex]
    texture = settings.TEXTURES[textureId]

    surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    surf.blit(texture, (0, 0), rect)
    return surf