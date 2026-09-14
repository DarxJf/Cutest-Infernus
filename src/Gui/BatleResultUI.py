from typing import List

import pygame

import settings
from src.Models.BattleEntity import BattleEntity


class BattleResultUI:
    def __init__(self, party: List[BattleEntity], earnedSouls: int, victory: bool) -> None:
        self.party = party
        self.earnedSouls = earnedSouls
        self.victory = victory

    def render(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        panelW, panelH = 300, 160
        panelX = (settings.VIRTUAL_WIDTH - panelW) // 2
        panelY = (settings.VIRTUAL_HEIGHT - panelH) // 2
        panelRect = pygame.Rect(panelX, panelY, panelW, panelH)

        pygame.draw.rect(surface, (20, 20, 30), panelRect, border_radius=6)
        border = (240, 220, 50) if self.victory else (200, 50, 80)
        pygame.draw.rect(surface, border, panelRect, width=2, border_radius=6)

        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

        titleText = "Victory!" if self.victory else "Defeat..."
        title = medium.render(titleText, True, border)
        surface.blit(title, title.get_rect(center=(settings.VIRTUAL_WIDTH / 2, panelY + 18)))

        y = panelY + 44

        if self.victory:
            soulsLine = small.render(f"Souls earned: {self.earnedSouls}", True, (200, 50, 100))
            surface.blit(soulsLine, (panelX + 16, y))
            y += 16

        for unit in self.party:
            if unit.dead:
                color = (120, 120, 120)
                line = f"{unit.classType}: DEFEATED"
            else:
                color = (220, 255, 220)
                line = f"{unit.classType}: Lv {unit.level}   EXP {int(unit.experience)}/{unit.experienceToNextLevel}"

            text = small.render(line, True, color)
            surface.blit(text, (panelX + 16, y))
            y += 14

        hint = small.render("Press Enter to continue", True, (150, 150, 150))
        surface.blit(hint, hint.get_rect(
            center=(settings.VIRTUAL_WIDTH / 2, panelY + panelH - 14)))