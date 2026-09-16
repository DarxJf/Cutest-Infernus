from typing import Any
import pygame

from gale.state import BaseState
from gale.save import SaveManager, SaveError

import settings
from src.Gui.Menu import Menu
from src.States.Game.SlotSelectState import SlotSelectState


class PauseMenuState(BaseState):
    def enter(self, runState=None, inBattle: bool = False) -> None:
        self.runState = runState
        self.inBattle = inBattle

        items = [("Continue", self.close)]
        if not inBattle:
            items.append(("Save game", self._save))
        items.append(("Load game" , self._load))
        items.append(("Quit game", self._quit))

        menuWidth = 160
        menuHeight = 100
        self.menuY = settings.VIRTUAL_HEIGHT / 2 - (menuHeight / 2)
        self.menu = Menu(
            settings.VIRTUAL_WIDTH / 2 - (menuWidth / 2),
            self.menuY,
            menuWidth,
            menuHeight,
            items=items,
            font=settings.FONTS["medium"],
        )

    def close(self) -> None:
        self.state_machine.pop()

    def _save(self) -> None:
        self.state_machine.push(
            SlotSelectState(self.state_machine),
            mode="save",
            onSelect=self._do_save,
        )

    def _do_save(self, slot: str) -> None:
        if self.runState is None:
            return

        try: 
            data = self.runState.to_dict()
            party = self.runState.party
            names = [getattr(m, "key", "?") for m in party.members if not m.dead]
            levels = [m.level for m in party.members if not m.dead]
            avgLevel = round(sum(levels) / len(levels), 1) if levels else 1
        except Exception as e:
            return

        try:
            SaveManager().save(
                slot,
                data,
                party_names = names,
                party_level = avgLevel,
                souls = self.runState.wallet.souls,
                battles = self.runState.battlesFought,
                )
        except Exception as e:
            return
        
        settings.SOUNDS["select"].play()

    def _load(self) -> None:
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

    def _quit(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))


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
           
            self.close()

    def render(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        medium = settings.FONTS["medium"]
        title_text = medium.render("PAUSE", True, (240, 220, 50))
        title_rect = title_text.get_rect(
            centerx=settings.VIRTUAL_WIDTH / 2, 
            bottom=self.menuY - 10
        )
        surface.blit(title_text, title_rect)

        self.menu.render(surface)