"""
Rest area: the safe hub between battles. Shows a campfire background
and a menu that opens Hire / Inventory / Actions submenus.
"""
from typing import Any

import pygame

from gale.state import BaseState

import settings
from src.Gui.Menu import Menu
from src.States.Game.HireState import HireState
from src.States.Game.FadeInState import FadeInState
from src.States.Game.FadeOutState import FadeOutState


class RestState(BaseState):
    def enter(
        self,
        runState,
    ) -> None:
        self.runState = runState

        for member in self.runState.party.members:
            if not member.dead:
                member.currentHp = member.hp
    
        self.runState.offers.reroll(self.runState.party)

        menuWidth = 160
        menuHeight = 100
        self.menuY = settings.VIRTUAL_HEIGHT / 2 - menuHeight / 2 + 10

        self.menu = Menu(
            settings.VIRTUAL_WIDTH / 2 - menuWidth / 2,
            self.menuY,
            menuWidth,
            menuHeight,
            items=[
                ("Hire companion", self._open_hire),
                ("Inventory",      self._open_inventory),
                ("Manage actions", self._open_actions),
                ("Shop",           self._open_shop), 
                ("Leave",          self._leave),
            ],
            font=settings.FONTS["medium"],
        )

        self.bgTexture = settings.TEXTURES.get("")


    def _open_hire(self) -> None:

        self.state_machine.push(
            HireState(self.state_machine),
            runState=self.runState,
            onClose=self._on_submenu_closed,
        )

    def _open_inventory(self) -> None:
        from src.States.Game.InventoryState import InventoryState
        self.state_machine.push(
            InventoryState(self.state_machine),
            runState=self.runState,
            onClose=self._on_submenu_closed,
        )

    def _open_actions(self) -> None:
        from src.States.Game.ManageActionState import ManageActionsState
        self.state_machine.push(
            ManageActionsState(self.state_machine),
            runState=self.runState,
            onClose=self._on_submenu_closed,
        )

    def _open_shop(self) -> None:
        from src.States.Game.ShopState import ShopState
        self.state_machine.push(
            ShopState(self.state_machine),
            runState=self.runState,
            onClose=self._on_submenu_closed,
        )

    def _leave(self) -> None:

        def on_complete() -> None:
            self.state_machine.pop()
            
            play_state = self.state_machine.states[-1]
            if hasattr(play_state,"regenerate_room"):
                play_state.regenerate_room()

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

    def _on_submenu_closed(self) -> None:
        pass


    def update(self, dt: float) -> None:
        self.menu.update(dt)

    
    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return

        if inputId == "moveUp":
            self.menu.navigate((0, -1))
        elif inputId == "moveDown":
            self.menu.navigate((0, 1))
        elif inputId == "enter":
            self.menu.confirm()
        elif inputId == "pause":
            self._leave()

    def render(self, surface: pygame.Surface) -> None:
        if self.bgTexture is not None:
            surface.blit(self.bgTexture, (0, 0))
        else:
            surface.fill((30, 20, 40))


        medium = settings.FONTS["medium"]
        title = medium.render("REST AREA", True, (240, 220, 50))
        surface.blit(title, title.get_rect(
            centerx=settings.VIRTUAL_WIDTH / 2,
            bottom=self.menuY - 10,
        ))

        small = settings.FONTS["small"]
        soulsText = small.render(f"Souls: {self.runState.wallet.souls}", True, (220, 220, 220))
        surface.blit(soulsText, (6, 6))

        partyText = small.render(
            f"Party: {self.runState.party.size()}/{4}", True, (220, 220, 220),
        )
        surface.blit(partyText, (settings.VIRTUAL_WIDTH - partyText.get_width() - 6, 6))

        self.menu.render(surface)