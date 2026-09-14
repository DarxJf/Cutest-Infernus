import pygame
import settings
from typing import List, Optional
from src.Models.BattleEntity import BattleEntity

class BattleUI:
    def __init__(self) -> None:
        self.selectedCardIndex = 0

    def render(
        self, 
        surface: pygame.Surface, 
        currentActor: Optional[BattleEntity], 
        upcomingTurns: List[BattleEntity]
    ) -> None:
        if currentActor:
            self._render_actor_info(surface, currentActor)
        
        self._render_turn_queue(surface, upcomingTurns)
        self._render_action_cards(surface, currentActor)

    def _render_actor_info(self, surface: pygame.Surface, actor: BattleEntity) -> None:
        container = pygame.Rect(5, 10, 140, 50)
        pygame.draw.rect(surface, (20, 20, 30), container, border_radius=5)
        pygame.draw.rect(surface, (200, 180, 50), container, width=1, border_radius=5)

        portraitRect = pygame.Rect(15, 15, 30, 40)
        pygame.draw.rect(surface, (80, 80, 100), portraitRect, border_radius=3)
        
        smallFont = settings.FONTS["small"]
        name_txt = smallFont.render(actor.classType[:12], True, (255, 255, 255))
        surface.blit(name_txt, (50, 15))

        hpPercent = max(0.0, min(1.0, actor.currentHp / actor.hp)) if actor.hp > 0 else 0
        bgBar = pygame.Rect(50, 32, 90, 8)
        fillBar = pygame.Rect(50, 32, int(90 * hpPercent), 8)
        
        pygame.draw.rect(surface, (60, 20, 20), bgBar, border_radius=2)
        pygame.draw.rect(surface, (200, 50, 100), fillBar, border_radius=2)

        hpTxt = smallFont.render(f"{actor.currentHp}/{actor.hp}", True, (255, 255, 255))
        surface.blit(hpTxt, (50, 42))

    def _render_turn_queue(self, surface: pygame.Surface, upcoming: List[BattleEntity]) -> None:
        startX = settings.VIRTUAL_WIDTH - 25
        startY = 10
        cardSize = 15

        for i, entity in enumerate(upcoming):
            x = startX - (i * (cardSize + 4))
            rect = pygame.Rect(x, startY, cardSize, cardSize)

            color = (50, 150, 250) if hasattr(entity, "is_party") and entity.is_party else (200, 50, 100)
            
            pygame.draw.rect(surface, (20, 20, 30), rect, border_radius=3)
            pygame.draw.rect(surface, color, rect, width=2, border_radius=3)

            smallFont = settings.FONTS["small"]
            initial = smallFont.render(entity.classType[0].upper(), True, (255, 255, 255))
            surface.blit(initial, initial.get_rect(center=rect.center))

    def _render_action_cards(self, surface: pygame.Surface, actor: Optional[BattleEntity]) -> None:
        cardsCount = len(actor.actionSlots) if actor and hasattr(actor, "actionSlots") and actor.actionSlots else 3
        cardW, card_h = 36, 48
        totalW = (cardsCount + 1) * (cardW + 6)
        startX = (settings.VIRTUAL_WIDTH - totalW) // 2
        startY = settings.VIRTUAL_HEIGHT - card_h - 10

        moveRect = pygame.Rect(startX, startY, cardW, card_h)
        isSelected = (self.selectedCardIndex == 0)
        
        pygame.draw.rect(surface, (30, 40, 60), moveRect, border_radius=4)
        borderColor = (240, 220, 50) if isSelected else (100, 100, 120)
        pygame.draw.rect(surface, borderColor, moveRect, width=2 if isSelected else 1, border_radius=4)

        smallFont = settings.FONTS["small"]
        txt = smallFont.render("Move", True, (255, 255, 255))
        surface.blit(txt, txt.get_rect(center=(moveRect.centerx, moveRect.centery)))

        for i in range(cardsCount):
            x = startX + (i + 1) * (cardW + 6)
            cardRect = pygame.Rect(x, startY, cardW, card_h)
            selected = (self.selectedCardIndex == i + 1)

            pygame.draw.rect(surface, (40, 30, 40), cardRect, border_radius=4)
            bCol = (240, 220, 50) if selected else (120, 100, 120)
            pygame.draw.rect(surface, bCol, cardRect, width=2 if selected else 1, border_radius=4)

            label = smallFont.render(f"Atk {i+1}", True, (220, 220, 220))
            surface.blit(label, label.get_rect(center=(cardRect.centerx, cardRect.centery)))