from typing import Any, Optional, Callable
import pygame
from gale.state import BaseState
import settings

CARD_WIDTH = 200
CARD_HEIGHT = 45
CARD_GAP = 12

class SlotSelectState(BaseState):
    def enter(
            self,
            mode: str = "load",
            onSelect: Optional[Callable[[str], None]] = None,
            onClose: Optional[Callable[[], None]] = None,
    ) -> None:
        self.mode = mode 
        self.onSelect = onSelect or (lambda slot: None)
        self.onClose = onClose or (lambda slot: None)

        self.selectedIndex = 0
        self.slots = settings.SAVE_SLOTS

        totalHeight = (CARD_HEIGHT * len(self.slots)) + (CARD_GAP * (len(self.slots) - 1))
        self.x = (settings.VIRTUAL_WIDTH - CARD_WIDTH) / 2
        self.top = (settings.VIRTUAL_HEIGHT - totalHeight) / 2

    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return

        if inputId == "moveUp":
            self.selectedIndex = (self.selectedIndex - 1) % len(self.slots)
            settings.SOUNDS["select"].play()
        elif inputId == "moveDown":
            self.selectedIndex = (self.selectedIndex + 1) % len(self.slots)
            settings.SOUNDS["select"].play()
        elif inputId == "enter":
            self._confirm()
        elif inputId == "pause":
            self._close()

    def _confirm(self) -> None:
        settings.SOUNDS["select"].play()
        chosenSlot = self.slots[self.selectedIndex]
        self.state_machine.pop()
        self.onSelect(chosenSlot)
    def _close(self) -> None:
        self.state_machine.pop()
        self.onClose()

    def render(self, surface: pygame.Surface) -> None:
     
        overlay = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        medium = settings.FONTS["medium"]
        titleText = "Save Game" if self.mode == "save" else "Load Game"
        title = medium.render(titleText, True, (240, 220, 50))
        titleRect = title.get_rect(center=(settings.VIRTUAL_WIDTH / 2, self.top - 25))
        surface.blit(title, titleRect)

        small = settings.FONTS["small"]

  
        for i, slotName in enumerate(self.slots):
            slotY = self.top + i * (CARD_HEIGHT + CARD_GAP)
            slotRect = pygame.Rect(self.x, slotY, CARD_WIDTH, CARD_HEIGHT)
            

            if i == self.selectedIndex:
                pygame.draw.rect(surface, (50, 50, 80), slotRect, border_radius=4)
                pygame.draw.rect(surface, (240, 220, 50), slotRect, width=2, border_radius=4)
                
                arrowRight = settings.FRAMES["cursors"][settings.TILE_IDS["arrowRight"]]
                surface.blit(settings.TEXTURES["cursors"], (self.x - 24, slotY + CARD_HEIGHT/2 - 8), arrowRight)
            else:
                pygame.draw.rect(surface, (30, 30, 30), slotRect, border_radius=4)
                pygame.draw.rect(surface, (100, 100, 100), slotRect, width=2, border_radius=4)

  
            text = small.render(f"{slotName} - Empty", True, (255, 255, 255))
            textRect = text.get_rect(centerx=settings.VIRTUAL_WIDTH / 2, centery=slotY + CARD_HEIGHT / 2)
            surface.blit(text, textRect)

        hint = small.render("PAUSE: Cancel", True, (150, 150, 150))
        hintRect = hint.get_rect(center=(settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT - 20))
        surface.blit(hint, hintRect)