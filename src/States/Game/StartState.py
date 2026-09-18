import pygame
from typing import Any 

from gale.state import BaseState
from gale.save import SaveError, SaveManager

import settings
from src.Gui.Menu import Menu
from src.States.Game.SelectCharacterState import SelectCharacterState
from src.States.Game.FadeInState import FadeInState
from src.States.Game.FadeOutState import FadeOutState
from src.States.Game.SlotSelectState import SlotSelectState


class StartState(BaseState):
    def enter(self) -> None:
        self.background = float = 0.0
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

        self.bgTexture = settings.TEXTURES["menu_bg"]
        self.bgWidth = self.bgTexture.get_width()  
        self.bgScrollSpeed = 20.0                   
        self.bgOffset = 0.0

        settings.play_music("main_CI")

    def update(self, dt):
        self.menu.update(dt)
        self.bgOffset = (self.bgOffset + self.bgScrollSpeed * dt) % self.bgWidth

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
        settings.stop_music("main_CI")
        self.state_machine.push(
            SlotSelectState(self.state_machine),
            mode="load",
            onSelect=self._do_load,
        )

    def _do_load(self, slot: str) -> None:     
        try:
            raw = SaveManager().load(slot)
        except SaveError:
            return

        save_data = raw.get("data", raw)

        self.state_machine.clear()
        from src.States.Game.PlayState import PlayState
        self.state_machine.push(
            PlayState(self.state_machine),
            run_state_dict=save_data,
        )

    def render(self, surface: pygame.Surface) -> None:
        x0 = -int(self.bgOffset)
        while x0 < settings.VIRTUAL_WIDTH:
            surface.blit(self.bgTexture, (x0, 0))
            x0 += self.bgWidth

        
        titleFont = settings.FONTS["large"]
    
        shadowSurf = titleFont.render("CUTEST INFERNO", True, (200, 50, 100))
        shadowRect = shadowSurf.get_rect(center = (settings.VIRTUAL_WIDTH / 2 + 1, settings.VIRTUAL_HEIGHT / 2 - 20 + 2))
        surface.blit(shadowSurf, shadowRect)

        title = titleFont.render("CUTEST INFERNO", True, (240, 220, 50))
        titleRect = title.get_rect(center = (settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 - 20))
        surface.blit(title, titleRect)

        self.menu.render(surface)

  


    