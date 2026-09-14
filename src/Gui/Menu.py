import pygame
from typing import Sequence, Tuple, Optional

from gale.ui.cursor import Cursor
from gale.ui.list_view import ListView
from gale.ui.theme import Theme

import settings



Item = Tuple[str, "callable"]

_MENU_THEME = Theme(
    background_color=pygame.Color(56, 56, 56),
    hover_color=pygame.Color(56, 56, 56),
    focus_color=pygame.Color(56, 56, 56),
    text_color=pygame.Color(255, 255, 255),
    border_width=0,
)

class Menu:
    def __init__(
            self,
            x: float,
            y: float,
            width: float,
            height: float,
            items: Sequence[Item],
            showCursor: bool = True,
            font: Optional[pygame.font.Font] = None,

            ) -> None:

        self.listView = ListView(
            x + 4,
            y + 3,
            width - 8,
            height - 6,
            items = items,
            font=font or settings.FONTS["medium"],
            cursor=None,
            theme=_MENU_THEME,
        )
        self.listView.focused = True

   
        cursorRect = settings.FRAMES["cursors"][settings.TILE_IDS["cursorRight"]]
        cursorSurface = settings.TEXTURES["cursors"].subsurface(cursorRect)
        self.cursor = Cursor(cursorSurface) if showCursor else None

    def update(self, dt:float) -> None:
        self.listView.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.listView.render(surface)

        if self.cursor is not None and self.listView.items:
            rowRect = self.listView.row_rect(self.listView.selected_index) 
            cursorX = self.listView.x - 10
            cursorY = rowRect.centery - 10
            self.cursor.render(surface, (cursorX, cursorY))

    
    def navigate(self, direction: Tuple[int, int]) -> None:
        dx, dy = direction
        if dy != 0:
            current = self.listView.selected_index
            target = current + dy
        if target < 0 or target >= len(self.listView.items):
            return

        if self.listView.on_navigate(direction):
            settings.SOUNDS["select"].stop()
            settings.SOUNDS["select"].play()


    def confirm(self) -> None:
        if self.listView.on_confirm():
            settings.SOUNDS["select"].stop()
            settings.SOUNDS["select"].play()