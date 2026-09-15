from typing import Any,List
import pygame

from gale.state import BaseState

import settings
from src.Definitions.Entity import get_main_characters
from src.States.Game.PlayState import PlayState

MAIN_ORDER: List[str] = ["Cloud", "Chloe", "Balthazar", "Pelusa"]

CHARACTER_COLORS = {
    "Chloe": (95, 22, 58),
    "Cloud": (50, 82, 95),
    "Balthazar": (74, 13, 24),
    "Pelusa": (96, 93, 36),
}

class SelectCharacterState(BaseState):
    def enter(
        self,
        characterIndex: int = 0,
    ) -> None:
        self.characterIndex = characterIndex
        mains = get_main_characters()
        self.mainKeys = [k for k in MAIN_ORDER if k in mains]

        self.bgTexture = settings.TEXTURES["menu_bg"]
        self.bgWidth = self.bgTexture.get_width()  
        self.bgScrollSpeed = 20.0                   
        self.bgOffset = 0.0

    def update(self, dt):
        self.bgOffset = (self.bgOffset + self.bgScrollSpeed * dt) % self.bgWidth
      
    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return
        
        if not self.mainKeys:
            return

        if inputId == "moveLeft":
            self.characterIndex = (self.characterIndex - 1) % len(MAIN_ORDER)
            settings.SOUNDS["select"].play()
        elif inputId == "moveRight":
            self.characterIndex = (self.characterIndex + 1) % len(MAIN_ORDER)
            settings.SOUNDS["select"].play()
        elif inputId == "enter":
            self._confirm()

    def _confirm(self) -> None:
        settings.SOUNDS["select"].play()
        chosenKey = self.mainKeys[self.characterIndex]
        self.state_machine.pop()
        self.state_machine.push(
            PlayState(self.state_machine),
            leader_key = chosenKey,
            )

    def render(self, surface: pygame.Surface) -> None:
        x0 = -int(self.bgOffset)
        surface.blit(self.bgTexture, (x0, 0))
        surface.blit(self.bgTexture, (x0 + self.bgWidth, 0))

        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

        centerX = settings.VIRTUAL_WIDTH / 2
        centerY = settings.VIRTUAL_HEIGHT / 2
   
        titleText = medium.render("SELECT CHARACTER", True, (240, 220, 50))
        titleRect = titleText.get_rect(centerx=centerX, y=16)
        surface.blit(titleText, titleRect)

        if not self.mainKeys:
            empty = medium.render("No main characters found", True, (200, 80, 80))
            surface.blit(empty, empty.get_rect(center=(centerX, centerY)))
            return

        chosenKey = self.mainKeys[self.characterIndex]
        adef = get_main_characters()[chosenKey]

        cardW, cardH = 150, 160
        cardRect = pygame.Rect(
            centerX - cardW / 2, centerY - cardH / 2 - 6, cardW, cardH
        )

        bg_color = CHARACTER_COLORS.get(chosenKey, (24, 24, 34))

        pygame.draw.rect(surface, bg_color, cardRect, border_radius=8)
        pygame.draw.rect(surface, (240, 220, 50), cardRect, width=2, border_radius=8)

        self._render_portrait(surface, chosenKey, cardRect)

        nameText = medium.render(chosenKey, True, (255, 255, 255))
        surface.blit(
            nameText,
            nameText.get_rect(centerx=cardRect.centerx, y=cardRect.bottom + 8),
        )

        classText = small.render(adef.get("class_name", ""), True, (200, 200, 200))
        surface.blit(
            classText,
            classText.get_rect(centerx=cardRect.centerx, y=cardRect.bottom + 26),
        )

        arrowRight = settings.FRAMES["cursors"][settings.TILE_IDS["arrowRight"]]
        arrowLeft = settings.FRAMES["cursors"][settings.TILE_IDS["arrowLeft"]]
        
        leftX = cardRect.left - 24
        rightX = cardRect.right + 8
        arrowY = cardRect.centery - arrowLeft.height / 2

        surface.blit(settings.TEXTURES["cursors"], (leftX, arrowY), arrowLeft)
        surface.blit(settings.TEXTURES["cursors"], (rightX, arrowY), arrowRight)

        startText = small.render("PRESS ENTER TO START GAME", True, (240, 220, 50))
        startRect = startText.get_rect(centerx=centerX, y=settings.VIRTUAL_HEIGHT - 20)
        surface.blit(startText, startRect)

    def _render_portrait(
        self, surface: pygame.Surface, key: str, cardRect: pygame.Rect,
    ) -> None:
      
        adef = get_main_characters()[key]
        textureId = adef.get("texture")
        if textureId is None or textureId not in settings.TEXTURES:
            return

        frameRect = None
        anims = adef.get("animations", {})
        idleDown = anims.get("idle-down") or anims.get("walk-down")
        if idleDown and "texture" in idleDown and "frames" in idleDown:
            framesList = idleDown["frames"]
            if framesList:
                frameIdx = framesList[0]
                frameRect = settings.FRAMES[idleDown["texture"]][frameIdx]
        if frameRect is None:
            frameIdx = adef.get("frame_index", 0)
            frameRect = settings.FRAMES[textureId][frameIdx]

        portrait = pygame.Surface(
            (frameRect.width, frameRect.height), pygame.SRCALPHA
        )
        portrait.blit(settings.TEXTURES[textureId], (0, 0), frameRect)

        scale = 3.0
        targetW = int(frameRect.width * scale)
        targetH = int(frameRect.height * scale)
        maxW = cardRect.width - 24
        maxH = cardRect.height - 24

        if targetW > maxW or targetH > maxH:
            ratio = min(maxW / targetW, maxH / targetH)
            targetW = int(targetW * ratio)
            targetH = int(targetH * ratio)

        portrait = pygame.transform.scale(portrait, (targetW, targetH))

        x = cardRect.centerx - targetW / 2
        y = cardRect.centery - targetH / 2
        surface.blit(portrait, (x, y))

   