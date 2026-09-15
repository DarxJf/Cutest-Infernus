"""
Submenu: shared inventory + equipping.

"""

from typing import Any

import pygame

from gale.state import BaseState

import settings
from src.Gui.Menu import Menu
from src.Definitions.Objects import PASSIVE_OBJECTS
from src.Utils.Icons import icon_surface
from src.Utils.TextUtils import wrap_text


class InventoryState(BaseState):
    def enter(
        self,
        runState,
        onClose=None,
    ) -> None:
        self.party = runState.party
        self.inventory = runState.inventory
        self.onClose = onClose or (lambda: None)

        self.focus = "items"
        self.selectedItemKey: str = None

        self._build_items_menu()
        self.membersMenu: Menu = None


    def _build_items_menu(self) -> None:
        itemKeys = self.inventory.all_keys()
        items = []

        for key in itemKeys:
            obj = self.inventory.items[key]
            items.append((obj.name, self._make_item_selector(key)))

        if not items:
            items.append(("(Empty)", lambda: None))

        items.append(("Back", self._close))

        menuW = 160
        menuH = settings.VIRTUAL_HEIGHT - 60
        self.itemsMenu = Menu(
            16,
            44,
            menuW,
            menuH,
            items=items,
            font=settings.FONTS["small"],
        )

    def _make_item_selector(self, key: str):
        def callback():
            self.selectedItemKey = key
            self._build_members_menu()
            self.focus = "members"
        return callback

    def _build_members_menu(self) -> None:
        items = []
        for i, member in enumerate(self.party.members):
            equipped = self.inventory.equipped_keys_for(i)
            label = f"{member.classType}  [{len(equipped)}/{member.slotObjects}]"
            items.append((label, self._make_member_callback(i)))
        items.append(("Cancel", self._cancel_selection))

        panelX = 188
        panelY = 44
        panelW = settings.VIRTUAL_WIDTH - panelX - 16
        panelH = settings.VIRTUAL_HEIGHT - 60

        self.membersMenu = Menu(
            panelX + 10,
            panelY + 40,
            panelW - 20,
            panelH - 50,
            items=items,
            font=settings.FONTS["small"],
        )

    def _make_member_callback(self, index: int):
        def callback():
            if self.selectedItemKey is None:
                return
            member = self.party.members[index]
            self.inventory.equip(self.selectedItemKey, index, member)
            settings.SOUNDS["select"].play()
            self._cancel_selection()
            self._build_items_menu()  
        return callback

    def _cancel_selection(self) -> None:
        self.selectedItemKey = None
        self.membersMenu = None
        self.focus = "items"

    def _close(self) -> None:
        self.state_machine.pop()
        self.onClose()


    def update(self, dt: float) -> None:
        self.itemsMenu.update(dt)
        if self.membersMenu:
            self.membersMenu.update(dt)

    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return

        activeMenu = self.membersMenu if self.focus == "members" else self.itemsMenu

        if inputId == "moveUp":
            activeMenu.navigate((0, -1))
        elif inputId == "moveDown":
            activeMenu.navigate((0, 1))
        elif inputId == "enter":
            activeMenu.confirm()
        elif inputId == "pause":
            if self.focus == "members":
                self._cancel_selection()
            else:
                self._close()


    def render(self, surface: pygame.Surface) -> None:
        surface.fill((15, 15, 22))

        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

        title = medium.render("Inventory", True, (240, 220, 50))
        surface.blit(title, (16, 12))

        partyText = small.render(f"Party: {len(self.party.members)}", True, (200, 200, 200))
        surface.blit(partyText, (settings.VIRTUAL_WIDTH - partyText.get_width() - 16, 16))


        self.itemsMenu.render(surface)

        self._render_right_column(surface)

    def _render_right_column(self, surface: pygame.Surface) -> None:
       
        panelX = 188
        panelY = 44
        panelW = settings.VIRTUAL_WIDTH - panelX - 16
        panelH = settings.VIRTUAL_HEIGHT - 60

        panelRect = pygame.Rect(panelX, panelY, panelW, panelH)
        pygame.draw.rect(surface, (20, 20, 30), panelRect, border_radius=4)
  
        borderColor = (240, 220, 50) if self.focus == "members" else (60, 60, 85)
        pygame.draw.rect(surface, borderColor, panelRect, width=1, border_radius=4)

        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

  
        if self.focus == "members":
            item_name = ""
            if self.selectedItemKey and self.selectedItemKey in PASSIVE_OBJECTS:
                item_name = PASSIVE_OBJECTS[self.selectedItemKey]["name"]

            header_str = f"Equip {item_name}:" if item_name else "Equip to:"
            header_lbl = medium.render(header_str, True, (240, 220, 50))
            surface.blit(header_lbl, (panelX + 10, panelY + 10))

            pygame.draw.line(surface, (40, 40, 60), (panelX + 10, panelY + 34), (panelX + panelW - 10, panelY + 34))

            if self.membersMenu:
                self.membersMenu.render(surface)
        else:
            itemKeys = self.inventory.all_keys()
            if not itemKeys:
                return

            idx = self.itemsMenu.listView.selected_index
            if idx >= len(itemKeys):
              
                return

            key = itemKeys[idx]
            objDef = PASSIVE_OBJECTS[key]
         
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