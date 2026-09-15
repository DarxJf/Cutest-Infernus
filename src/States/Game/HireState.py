
"""
Submenu: hire a secondary companion from today's offer.
"""

from typing import Any, Optional

import pygame

from gale.state import BaseState

import settings
from src.Gui.Menu import Menu
from src.Models.Party import MAX_PARTY_SIZE
from src.Definitions.Entity import PLAYER_CHARACTERS
from src.Utils.Icons import icon_surface
from src.Utils.TextUtils import wrap_text


DEFAULT_HIRE_COST = 80


class HireState(BaseState):
    def enter(
        self,
        runState,
        onClose=None,
    ) -> None:
        self.runState = runState
        self.onClose = onClose or (lambda: None)

        self.replaceMenu: Optional[Menu] = None
        self.pendingKey: Optional[str] = None
        self.pendingCost: int = 0

        self._build_menu()

    def _build_menu(self) -> None:
        items = []
        for key in self.runState.offers.all():
            adef = PLAYER_CHARACTERS[key]
            cost = self._cost_of(key)
            label = f"{key}  ({cost})"
            items.append((label, self._make_hire_callback(key, cost)))

        if not items:
            items.append(("(No one is around today)", lambda: None))

        items.append(("Back", self._close))

        menuW = 160
        menuH = settings.VIRTUAL_HEIGHT - 60
        self.menuFont = settings.FONTS["small"]

        self.menu = Menu(
            16,
            44,
            menuW,
            menuH,
            items=items,
            font=self.menuFont,
        )

    def _cost_of(self, key: str) -> int:
        return PLAYER_CHARACTERS[key].get("hire_cost", DEFAULT_HIRE_COST)

    def _make_hire_callback(self, key: str, cost: int):
        def cb():
            if self.runState.party.has(key):
                settings.SOUNDS["select"].play()
                return
            if self.runState.wallet.souls < cost:
                settings.SOUNDS["select"].play()
                return

            if self.runState.party.is_full():
                self._ask_replacement(key, cost)
            else:
                self._perform_hire(key, cost)
        return cb

    def _perform_hire(self, key: str, cost: int) -> None:
        self.runState.wallet.souls -= cost
        self.runState.party.hire(key)
        self.runState.offers.remove(key)
        settings.SOUNDS["select"].play()
        self._build_menu()

    def _ask_replacement(self, key: str, cost: int) -> None:
        self.pendingKey = key
        self.pendingCost = cost

        items = []
        for i in self.runState.party.secondaryIndexes():
            member = self.runState.party.members[i]
            items.append((member.key, self._make_dismiss_callback(i)))
        items.append(("Cancel", self._cancel_replacement))

        panelX = 188
        panelY = 44
        panelW = settings.VIRTUAL_WIDTH - panelX - 16
        panelH = settings.VIRTUAL_HEIGHT - 60

        self.replaceMenu = Menu(
            panelX + 10,
            panelY + 40,
            panelW - 20,
            panelH - 50,
            items=items,
            font=settings.FONTS["small"],
        )

    def _make_dismiss_callback(self, index: int):
        def cb():
            if self.runState.wallet.souls < self.pendingCost:
                return
            self.runState.wallet.souls -= self.pendingCost
            self.runState.party.hire(self.pendingKey, replaceIndex=index)
            self.runState.offers.remove(self.pendingKey)
            settings.SOUNDS["select"].play()
            self._cancel_replacement()
            self._build_menu()
        return cb

    def _cancel_replacement(self) -> None:
        self.pendingKey = None
        self.pendingCost = 0
        self.replaceMenu = None

    def _close(self) -> None:
        self.state_machine.pop()
        self.onClose()

    def update(self, dt: float) -> None:
        if self.replaceMenu:
            self.replaceMenu.update(dt)
        else:
            self.menu.update(dt)

    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return

        activeMenu = self.replaceMenu if self.replaceMenu else self.menu
        if inputId == "moveUp":
            activeMenu.navigate((0, -1))
        elif inputId == "moveDown":
            activeMenu.navigate((0, 1))
        elif inputId == "enter":
            activeMenu.confirm()
        elif inputId == "pause":
            if self.replaceMenu:
                self._cancel_replacement()
            else:
                self._close()


    def render(self, surface: pygame.Surface) -> None:
        surface.fill((15, 15, 22))

        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

        title_str = "Replace Companion" if self.replaceMenu else "Hire Companion"
        title = medium.render(title_str, True, (240, 220, 50))
        surface.blit(title, (16, 12))

        right_margin = settings.VIRTUAL_WIDTH - 16
        partyText = small.render(f"Party: {self.runState.party.size()}/{MAX_PARTY_SIZE}", True, (200, 200, 200))
        soulsText = small.render(f"Souls: {self.runState.wallet.souls}", True, (240, 220, 50))

        surface.blit(partyText, (right_margin - partyText.get_width(), 16))
        surface.blit(soulsText, (right_margin - partyText.get_width() - soulsText.get_width() - 16, 16))

        self.menu.render(surface)

        self._render_right_column(surface)

    def _render_right_column(self, surface: pygame.Surface) -> None:
       
        panelX = 188
        panelY = 44
        panelW = settings.VIRTUAL_WIDTH - panelX - 16
        panelH = settings.VIRTUAL_HEIGHT - 60

        panelRect = pygame.Rect(panelX, panelY, panelW, panelH)
        pygame.draw.rect(surface, (20, 20, 30), panelRect, border_radius=4)

        borderColor = (240, 220, 50) if self.replaceMenu else (60, 60, 85)
        pygame.draw.rect(surface, borderColor, panelRect, width=1, border_radius=4)

        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

        if self.replaceMenu:
            header_lbl = medium.render("Replace who?", True, (240, 220, 50))
            surface.blit(header_lbl, (panelX + 10, panelY + 10))

            pygame.draw.line(surface, (40, 40, 60), (panelX + 10, panelY + 34), (panelX + panelW - 10, panelY + 34))

            self.replaceMenu.render(surface)
            return

        keys = self.runState.offers.all()
        if not keys:
            return

        idx = self.menu.listView.selected_index
        if idx >= len(keys):
            return

        key = keys[idx]
        adef = PLAYER_CHARACTERS[key]
        cost = self._cost_of(key)
        affordable = self.runState.wallet.souls >= cost
        is_in_party = self.runState.party.has(key)

        iconSize = 32
        textureId = adef.get("texture")
        frameIndex = adef.get("frame_index", 0)
        if textureId is not None:
            icon = icon_surface(textureId, frameIndex)
            if icon is not None:
                icon = pygame.transform.scale(icon, (iconSize, iconSize))
                surface.blit(icon, (panelX + 10, panelY + 10))

    
        nameX = panelX + 10 + iconSize + 10
        nameLines = wrap_text(medium, key, panelW - (iconSize + 30))
        y = panelY + 8
        for line in nameLines:
            name_lbl = medium.render(line, True, (255, 255, 255))
            surface.blit(name_lbl, (nameX, y))
            y += medium.get_height()

        if is_in_party:
            statusText = small.render("[ ALREADY IN PARTY ]", True, (150, 150, 150))
        elif not affordable:
            statusText = small.render(f"Cost: {cost} Souls (Low Souls)", True, (220, 100, 100))
        else:
            statusText = small.render(f"{adef.get('class_name', 'Companion')}  ({cost} Souls)", True, (240, 220, 50))
        surface.blit(statusText, (nameX, y + 2))

        contentY = panelY + 50
        pygame.draw.line(surface, (40, 40, 60), (panelX + 10, contentY), (panelX + panelW - 10, contentY))

        textY = contentY + 8
        lineH = small.get_height() + 2

        statsLine1 = f"HP {adef.get('base_hp', 0)}   ATK {adef.get('base_attack', 0)}"
        statsLine2 = f"DEF {adef.get('base_defense', 0)}   MAG {adef.get('base_magic', 0)}"

        lbl1 = small.render(statsLine1, True, (150, 220, 150))
        surface.blit(lbl1, (panelX + 10, textY))
        textY += lineH

        lbl2 = small.render(statsLine2, True, (150, 220, 150))
        surface.blit(lbl2, (panelX + 10, textY))
        textY += lineH + 6

        if not is_in_party and affordable:
            if self.runState.party.is_full():
                hint = small.render("ENTER: Select companion to replace", True, (200, 200, 200))
            else:
                hint = small.render("ENTER: Hire companion", True, (200, 200, 200))
            surface.blit(hint, (panelX + 10, textY))