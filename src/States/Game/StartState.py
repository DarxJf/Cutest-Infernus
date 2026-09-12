import pygame
from typing import Any 

from gale.state import BaseState

import settings
from src.Gui.Menu import Menu
from src.States.Game.SelectCharacterState import SelectCharacterState
from src.States.Game.FadeInState import FadeInState
from src.States.Game.FadeOutState import FadeOutState
from src.States.Game.SlotSelectState import SlotSelectState

class StartState(BaseState):
    def enter(self) -> None:
        self.menu = Menu(
            settings.VIRTUAL_WIDTH / 2  - 70,
            settings.VIRTUAL_HEIGHT /2 + 20,
            140,
            48,
            items=[ 
                ("New game", self._start_new_game),
                ("Load game", self._load_game),
            ],
            font = settings.FONTS["medium"],
        )

    def update(self, dt):
        self.menu.update(dt)

    def on_input(self, input_id: str, input_data: Any) ->None:
        if not input_data.pressed:
            return
        if input_id == "moveUp":
            self.menu.navigate((0, -1))
        elif input_id == "moveDown":
            self.menu.navigate((0, 1))
        elif input_id == "enter":
            self.menu.confirm()

    def _start_new_game(self) -> None:

        def on_complete() -> None:
            self.state_machine.pop()
            self.state_machine.push(SelectCharacterState(self.state_machine))

            self.state_machine.push(
                FadeOutState(self.state_machine),
                color=(0, 0, 0),
                time=0.5,
                onComplete=lambda: None,
            )

        self.state_machine.push(
            FadeInState(self.state_machine),
            color=(0, 0, 0),
            time=1,
            onComplete=on_complete,
        )


    def _load_game(self) -> None:
        self.state_machine.push(SlotSelectState(self.state_machine), mode="load")

    def render(self, surface: pygame.Surface) -> None:
      
        titleFont = settings.FONTS["large"]
    
        shadowSurf = titleFont.render("CUTEST INFERNO", True, (200, 50, 100))
        shadowRect = shadowSurf.get_rect(center = (settings.VIRTUAL_WIDTH / 2 + 1, settings.VIRTUAL_HEIGHT / 2 - 20 + 2))
        surface.blit(shadowSurf, shadowRect)

        title = titleFont.render("CUTEST INFERNO", True, (240, 220, 50))
        titleRect = title.get_rect(center = (settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 - 20))
        surface.blit(title, titleRect)

        self.menu.render(surface)

    



    