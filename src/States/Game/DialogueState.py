
from typing import Any, Callable, Optional

import pygame

from gale.state import BaseState
from gale.ui.text_box import TextBox

import settings
from src.Gui.Themes import DIALOGUE_THEME


class DialogueState(BaseState):
    def enter(
        self,
        text: str = "",
        onClose: Optional[Callable[[], None]] = None,
        position: str = "bottom",
        linesPerPage: int = 2,
    ) -> None:
        self._onClose = onClose or (lambda: None)

        panelWidth = settings.VIRTUAL_WIDTH - 12
        panelHeight = 64

        if position == "bottom":
            panelX, panelY = 6, settings.VIRTUAL_HEIGHT - panelHeight - 6
        elif position == "top":
            panelX, panelY = 6, 6
        else:   
            panelX = 6
            panelY = (settings.VIRTUAL_HEIGHT - panelHeight) // 2

        self.textbox = TextBox(
            panelX,
            panelY,
            panelWidth,
            panelHeight,
            text,
            font=settings.FONTS["small"],
            lines_per_page=linesPerPage,
            on_close=self._onTextboxClose,
            theme=DIALOGUE_THEME
        )

    def _onTextboxClose(self) -> None:
        self.state_machine.pop()
        self._onClose()


    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return

        if inputId in ("enter", "space"):
            self.textbox.advance()
        elif inputId == "pause":
         
            self._onTextboxClose()

    def render(self, surface: pygame.Surface) -> None:
        self.textbox.render(surface)