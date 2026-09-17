"""
Game-specific themes for gale UI widgets.

"""

import pygame
import settings

from gale.ui.theme import Theme

DIALOGUE_THEME = Theme(
    font=settings.FONTS["small"],
    text_color=pygame.Color(255, 255, 255),
    background_color=pygame.Color(20, 20, 30),        
    border_color=pygame.Color(240, 220, 50),          
    border_width=2,
    accent_color=pygame.Color(255, 200, 80),
    padding=8,
)