import pygame
import settings
from typing import List, Optional
from src.Definitions.Entity import PLAYER_CHARACTERS, ENEMIES
from src.Models.BattleEntity import BattleEntity
from src.Utils.Icons import icon_surface

class BattleUI:
    def __init__(self) -> None:
        self.selectedCardIndex = 0

    def render(
        self, 
        surface: pygame.Surface, 
        currentActor: Optional[BattleEntity], 
        upcomingTurns: List[BattleEntity],
        hasMoved: bool = False
    ) -> None:
        if currentActor:
            self._render_actor_info(surface, currentActor)
        
        self._render_turn_queue(surface, upcomingTurns)
        self._render_action_cards(surface, currentActor, hasMoved)

    def _portrait_surface(self, entity: BattleEntity, size: int = 24) -> Optional[pygame.Surface]:
       
        textureId = None
        frameIndex = 0

        key = getattr(entity, "key", None)
        if key and key in PLAYER_CHARACTERS:
            adef = PLAYER_CHARACTERS[key]
            textureId = adef.get("texture")
            frameIndex = adef.get("frame_index", 0)

        if textureId is None and entity.classType:
            enemyKey = entity.classType.lower()
            if enemyKey in ENEMIES:
                edef = ENEMIES[enemyKey]
                anims = edef.get("animations", {})
                idle = anims.get("idle-down") or anims.get("default")
                if idle and "texture" in idle and "frames" in idle and idle["frames"]:
                    textureId = idle["texture"]
                    frameIndex = idle["frames"][0]

        if textureId is None:
            textureId = getattr(entity, "currentTextureId", None) or getattr(entity, "textureId", None)
            frameIndex = getattr(entity, "frameIndex", 0)

        if textureId is None:
            return None

        icon = icon_surface(textureId, frameIndex)
        if icon is None:
            return None

        return pygame.transform.scale(icon, (size, size))



    def _render_actor_info(self, surface: pygame.Surface, actor: BattleEntity) -> None:
        container = pygame.Rect(5, 10, 140, 50)
        pygame.draw.rect(surface, (20, 20, 30), container, border_radius=5)
        pygame.draw.rect(surface, (200, 180, 50), container, width=1, border_radius=5)

        portrait = self._portrait_surface(actor, size=40)
        portraitRect = pygame.Rect(15, 15, 30, 40)
        pygame.draw.rect(surface, (80, 80, 100), portraitRect, border_radius=3)

        if portrait is not None:
            px = portraitRect.centerx - portrait.get_width() // 2
            py = portraitRect.centery - portrait.get_height() // 2
            surface.blit(portrait, (px, py))

        
        smallFont = settings.FONTS["small"]
        nameText = getattr(actor, "key", None) or actor.classType
        name_txt = smallFont.render(nameText[:14], True, (255, 255, 255))
        surface.blit(name_txt, (60, 16))

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
        cardSize = 24
        smallFont = settings.FONTS["small"]

        for i, entity in enumerate(upcoming):
            x = startX - (i * (cardSize + 4))
            rect = pygame.Rect(x, startY, cardSize, cardSize)

            color = (50, 150, 250) if hasattr(entity, "is_party") and entity.is_party else (200, 50, 100)
            
            pygame.draw.rect(surface, (20, 20, 30), rect, border_radius=3)
            pygame.draw.rect(surface, color, rect, width=2, border_radius=3)

            portrait = self._portrait_surface(entity, size=cardSize - 6)
            if portrait is not None:
                px = rect.centerx - portrait.get_width() // 2
                py = rect.centery - portrait.get_height() // 2
                surface.blit(portrait, (px, py))
            else:
                initial = smallFont.render(
                    entity.classType[0].upper(), True, (255, 255, 255),
                )
                surface.blit(initial, initial.get_rect(center=rect.center))

    def _render_action_cards(
        self,
        surface: pygame.Surface,
        actor: Optional[BattleEntity],
        hasMoved: bool,
    ) -> None:
        if not actor:
            return

        cards = [("Move", None, None, 0)]

        if hasattr(actor, "basicAttack") and actor.basicAttack:
            basic = actor.basicAttack
            cards.append((
                basic.name,
                basic,
                getattr(basic, "textureId", None),
                getattr(basic, "frameIndex", 0),
            ))

        for action in actor.actionSlots:
            cards.append((
                action.name,
                action,
                getattr(action, "textureId", None),
                getattr(action, "frameIndex", 0),
            ))

        cards.append(("Pass", None, None, 0))

        cardsCount = len(cards)
        cardW, cardH = 42, 48
        totalW = cardsCount * (cardW + 6)
        startX = (settings.VIRTUAL_WIDTH - totalW) // 2
        startY = settings.VIRTUAL_HEIGHT - cardH - 10

        smallFont = settings.FONTS["small"]

        for i, (labelText, action_obj, iconTexId, iconFrame) in enumerate(cards):
            x = startX + i * (cardW + 6)
            cardRect = pygame.Rect(x, startY, cardW, cardH)
            isSelected = (self.selectedCardIndex == i)

            if labelText == "Pass":
                bg_color = (255, 140, 0) if not isSelected else (255, 180, 50)
            elif i == 0:
                bg_color = (30, 40, 60)
            else:
                bg_color = (40, 30, 40)

            pygame.draw.rect(surface, bg_color, cardRect, border_radius=4)
            bCol = (240, 220, 50) if isSelected else (120, 100, 120)
            pygame.draw.rect(
                surface, bCol, cardRect,
                width=2 if isSelected else 1, border_radius=4,
            )

            iconSize = 20
            iconX = cardRect.centerx - iconSize // 2
            iconY = cardRect.top + 4

            icon = icon_surface(iconTexId, iconFrame) if iconTexId else None
            if icon is not None:
                icon = pygame.transform.scale(icon, (iconSize, iconSize))
                surface.blit(icon, (iconX, iconY))

            label = smallFont.render(
                labelText[:6], True,
                (255, 255, 255) if isSelected else (220, 220, 220),
            )
            labelY = cardRect.bottom - label.get_height() - 2
            surface.blit(
                label, label.get_rect(centerx=cardRect.centerx, bottom=labelY + label.get_height()),
            )

            isBlocked = False
            overlayText = ""

            if action_obj is not None:
                cooldown_turns = actor.skillCooldowns.get(action_obj.name, 0)
                if cooldown_turns > 0:
                    isBlocked = True
                    overlayText = str(cooldown_turns)
            elif labelText == "Move" and hasMoved:
                isBlocked = True

            if isBlocked:
                veil = pygame.Surface((cardW, cardH), pygame.SRCALPHA)
                veil.fill((0, 0, 0, 180))
                surface.blit(veil, (cardRect.x, cardRect.y))

                if overlayText:
                    cd_font = settings.FONTS["medium"]
                    cd_text = cd_font.render(overlayText, True, (255, 50, 50))
                    surface.blit(cd_text, cd_text.get_rect(center=cardRect.center))
