from typing import Any
import pygame

import settings

class ActionInfoPanel:
    @staticmethod
    def render(surface: pygame.Surface, action: Any, x: int, y: int, width: int = 220) -> None:
        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

        desc_text = getattr(action, "description", "Sssshhh, nothing to read.")
        desc_lines = ActionInfoPanel._wrap_text(desc_text, small, width - 20)
        
        # rect
        header_height = 30
        stats_height = 60
        desc_height = len(desc_lines) * (small.get_height() + 2)
        total_height = header_height + stats_height + desc_height + 20

        # draw bg and border
        panel_rect = pygame.Rect(x, y, width, total_height)
        pygame.draw.rect(surface, (20, 20, 30, 240), panel_rect, border_radius=6)
        pygame.draw.rect(surface, (240, 220, 50), panel_rect, width=1, border_radius=6)

        # name
        title_lbl = medium.render(action.name.replace("_", " ").title(), True, (240, 220, 50))
        surface.blit(title_lbl, (x + 10, y + 10))
        pygame.draw.line(surface, (60, 60, 85), (x + 10, y + 32), (x + width - 10, y + 32))

        # parameters
        stat_y = y + 40
        
        target_str = f"Target: {action.targetType.capitalize()} ({action.areaType})"
        target_lbl = small.render(target_str, True, (200, 200, 200))
        surface.blit(target_lbl, (x + 10, stat_y))
        
        range_str = f"Range: {action.gridRange}"
        range_lbl = small.render(range_str, True, (200, 200, 200))
        surface.blit(range_lbl, (x + width - 10 - range_lbl.get_width(), stat_y))
        
        stat_y += 18
        
        scale_str = f"Stat: {action.scalingStat.capitalize()} (x{action.multiplier})"
        scale_lbl = small.render(scale_str, True, (150, 220, 150))
        surface.blit(scale_lbl, (x + 10, stat_y))

        cd_str = f"CD: {action.cooldown} turns" if action.cooldown > 0 else "CD: instant"
        cd_lbl = small.render(cd_str, True, (220, 150, 150) if action.cooldown > 0 else (200, 200, 200))
        surface.blit(cd_lbl, (x + width - 10 - cd_lbl.get_width(), stat_y))

        if getattr(action, "effect", None):
            stat_y += 18
            eff_lbl = small.render(f"Effect: {action.effect.capitalize()}", True, (200, 150, 255))
            surface.blit(eff_lbl, (x + 10, stat_y))

        # Description
        pygame.draw.line(surface, (60, 60, 85), (x + 10, stat_y + 20), (x + width - 10, stat_y + 20))
        text_y = stat_y + 28
        for line in desc_lines:
            line_lbl = small.render(line, True, (180, 180, 180))
            surface.blit(line_lbl, (x + 10, text_y))
            text_y += small.get_height() + 2

    @staticmethod
    def _wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list:
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines