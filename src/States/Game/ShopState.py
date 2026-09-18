
"""
Submenu: buy passive objects with souls.
"""
from typing import Any

import pygame

from gale.state import BaseState

import settings
from src.Gui.Menu import Menu
from src.Models.Inventory import Inventory
from src.Definitions.Objects import PASSIVE_OBJECTS
from src.Utils.Icons import icon_surface
from src.Utils.TextUtils import wrap_text

SHOP_COSTS = {
    "vitality_ring": 60,
    "sage_necklace": 70,
    "brute_belt":    90,
    "swift_boots":   80,
  
    "iron_sword": 65,
    "iron_shield": 65,
    "swift_charm": 70,
    "arcane_orb": 75,

    "assassin_dagger": 110,
    "guardian_plate": 120,
    "wind_cloak": 110,
    "warlock_tome": 130,

    "hero_medal": 180,
    "cursed_ring": 200,
}

class ShopState(BaseState):
    def enter(self, runState, onClose=None) -> None:
        self.runState = runState
        self.inventory = runState.inventory
        self.onClose = onClose or (lambda: None)

        self.shopKeys = list(PASSIVE_OBJECTS.keys())

        items = []
        for key in self.shopKeys:
            adef = PASSIVE_OBJECTS[key]
            cost = SHOP_COSTS.get(key, 100)
            label = f"{adef['name']}  ({cost})"
            items.append((label, self._make_buy_callback(key, cost)))
        items.append(("Back", self._close))

        menuW = 160
        menuH = settings.VIRTUAL_HEIGHT - 60
        self.menu = Menu(
            16,
            44,
            menuW,
            menuH,
            items=items,
            font=settings.FONTS["small"],
        )

    def _make_buy_callback(self, key: str, cost: int):
        def cb():
            if self.runState.wallet.souls < cost:
                settings.SOUNDS["select"].play()
                return
            if self.inventory.has(key):
                return
            self.runState.wallet.souls -= cost
            self.inventory.add(key)
            settings.SOUNDS["select"].play()
        return cb

    def _close(self) -> None:
        self.state_machine.pop()
        self.onClose()

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
            self._close()

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((15, 15, 22))

        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

        title = medium.render("Shop", True, (240, 220, 50))
        surface.blit(title, (16, 12))

        
        soulsText = small.render(f"Souls: {self.runState.wallet.souls}", True, (240, 220, 50))
        surface.blit(soulsText, (settings.VIRTUAL_WIDTH - soulsText.get_width() - 16, 16))

     
        self.menu.render(surface)

        self._render_item_detail(surface)

    def _render_item_detail(self, surface: pygame.Surface) -> None:
     
        panelX = 188
        panelY = 44
        panelW = settings.VIRTUAL_WIDTH - panelX - 16
        panelH = settings.VIRTUAL_HEIGHT - 60

        panelRect = pygame.Rect(panelX, panelY, panelW, panelH)
        pygame.draw.rect(surface, (20, 20, 30), panelRect, border_radius=4)
        pygame.draw.rect(surface, (60, 60, 85), panelRect, width=1, border_radius=4)

   
        idx = self.menu.listView.selected_index
        if idx >= len(self.shopKeys):
            return

        key = self.shopKeys[idx]
        objDef = PASSIVE_OBJECTS[key]
        cost = SHOP_COSTS.get(key, 100)
        is_owned = self.inventory.has(key)

        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

        iconSize = 32
        icon = icon_surface(objDef["texture_id"], objDef["frame_index"])
        if icon is not None:
            icon = pygame.transform.scale(icon, (iconSize, iconSize))
            surface.blit(icon, (panelX + 10, panelY + 10))

  
        nameX = panelX + 10 + iconSize + 10
        nameLines = wrap_text(medium, objDef["name"], panelW - (iconSize + 30))
        y = panelY + 8
        for line in nameLines:
            name_lbl = medium.render(line, True, (255, 255, 255))
            surface.blit(name_lbl, (nameX, y))
            y += medium.get_height()

        if is_owned:
            statusText = small.render("[ OWNED ]", True, (120, 200, 120))
        else:
            statusText = small.render(f"Cost: {cost} Souls", True, (240, 220, 50))
        surface.blit(statusText, (nameX, y + 2))

      
        contentY = panelY + 50
        pygame.draw.line(surface, (40, 40, 60), (panelX + 10, contentY), (panelX + panelW - 10, contentY))

        textAreaW = panelW - 20
        descLines = wrap_text(small, objDef["description"], textAreaW)
        
        textY = contentY + 8
        lineH = small.get_height() + 2
        for line in descLines:
            desc_lbl = small.render(line, True, (200, 200, 200))
            surface.blit(desc_lbl, (panelX + 10, textY))
            textY += lineH

        textY += 6
        statsText = "   ".join(f"{k}+{v}" for k, v in objDef["stat_modifiers"].items())
        statsLines = wrap_text(small, statsText, textAreaW)
        for line in statsLines:
            stats_lbl = small.render(line, True, (150, 220, 150))
            surface.blit(stats_lbl, (panelX + 10, textY))
            textY += lineH