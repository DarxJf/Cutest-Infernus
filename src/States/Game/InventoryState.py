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

        self.focus = "items" # itemns or member
        self.active_zone = 0
        self.item_idx = 0
        
        self.selectedItemKey: str = None
        self.isUnequipping = False 

        self.membersMenu = None

    def _build_members_menu(self) -> None:
        items = []
        for i, member in enumerate(self.party.members):
            equipped = self.inventory.equipped_keys_for(i)
            label = f"{member.classType}  [{len(equipped)}/{member.slotObjects}]"

            if self.isUnequipping:
                if len(equipped) > 0:
                    items.append((label, self._make_member_unequip_callback(i)))
                else:
                    items.append((label + " (Vacío)", lambda: None))
            else:
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
        return callback

    def _make_member_unequip_callback(self, index: int):
        def callback():
            member = self.party.members[index]
            equipped = self.inventory.equipped_keys_for(index)
            
            if equipped:
                item_key = equipped[0] 

                self.inventory.unequip(item_key, index, member) 
                settings.SOUNDS["select"].play()
                
            self._cancel_selection()
        return callback

    def _cancel_selection(self) -> None:
        self.selectedItemKey = None
        self.isUnequipping = False
        self.membersMenu = None
        self.focus = "items"

        any_equipped = any(
            len(self.inventory.equipped_keys_for(i)) > 0 
            for i in range(len(self.party.members))
        )
        if self.active_zone == 1 and not any_equipped:
            self.active_zone = 0

    def _close(self) -> None:
        self.state_machine.pop()
        self.onClose()

    def update(self, dt: float) -> None:
        if self.membersMenu and self.focus == "members":
            self.membersMenu.update(dt)

    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return

        if self.focus == "items":
            any_equipped = any(
                len(self.inventory.equipped_keys_for(i)) > 0 
                for i in range(len(self.party.members))
            )

            if inputId == "moveUp":
                if self.active_zone == 2:
                    self.active_zone = 1 if any_equipped else 0
                elif self.active_zone == 1:
                    self.active_zone = 0
                if "select" in settings.SOUNDS: settings.SOUNDS["select"].play()
                
            elif inputId == "moveDown":
                if self.active_zone == 0:
                    self.active_zone = 1 if any_equipped else 2
                elif self.active_zone == 1:
                    self.active_zone = 2
                if "select" in settings.SOUNDS: settings.SOUNDS["select"].play()
                
            elif inputId == "moveLeft" and self.active_zone == 0:
                self.item_idx = max(0, self.item_idx - 1)
                if "select" in settings.SOUNDS: settings.SOUNDS["select"].play()
            elif inputId == "moveRight" and self.active_zone == 0:
                item_keys = self.inventory.all_keys()
                if item_keys:
                    self.item_idx = min(len(item_keys) - 1, self.item_idx + 1)
                if "select" in settings.SOUNDS: settings.SOUNDS["select"].play()
                
            elif inputId == "enter":
                if "select" in settings.SOUNDS: settings.SOUNDS["select"].play()
                
                if self.active_zone == 0:
                    item_keys = self.inventory.all_keys()
                    if item_keys:
                        self.selectedItemKey = item_keys[self.item_idx]
                        self.isUnequipping = False
                        self.focus = "members"
                        self._build_members_menu()
                        
                elif self.active_zone == 1:
                    if any_equipped:
                        self.selectedItemKey = None
                        self.isUnequipping = True
                        self.focus = "members"
                        self._build_members_menu()
                    else:
                        if "error" in settings.SOUNDS: settings.SOUNDS["error"].play()
                        
                elif self.active_zone == 2:
                    self._close()
                    
            elif inputId in ["pause", "undo"]:
                self._close()

        elif self.focus == "members":
            if inputId == "moveUp":
                self.membersMenu.navigate((0, -1))
            elif inputId == "moveDown":
                self.membersMenu.navigate((0, 1))
            elif inputId == "enter":
                self.membersMenu.confirm()
            elif inputId in ["pause", "undo"]:
                self._cancel_selection()

        elif self.focus == "members":
            if inputId == "moveUp":
                self.membersMenu.navigate((0, -1))
            elif inputId == "moveDown":
                self.membersMenu.navigate((0, 1))
            elif inputId == "enter":
                self.membersMenu.confirm()
            elif inputId in ["pause", "undo"]:
                self._cancel_selection()

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((15, 15, 22))

        medium = settings.FONTS["medium"]
        small = settings.FONTS["small"]

        title = medium.render("Inventory", True, (240, 220, 50))
        surface.blit(title, (16, 12))

        partyText = small.render(f"Party: {len(self.party.members)}", True, (200, 200, 200))
        surface.blit(partyText, (settings.VIRTUAL_WIDTH - partyText.get_width() - 16, 16))

        self._render_left_column(surface)
        self._render_right_column(surface)

    def _render_left_column(self, surface: pygame.Surface) -> None:
        font = settings.FONTS["small"]
        
        # Zone 0
        c_color = (240, 220, 50) if self.focus == "items" and self.active_zone == 0 else (100, 100, 100)
        surface.blit(font.render("Select Item:", True, (200, 200, 200)), (16, 60))
        
        item_keys = self.inventory.all_keys()
        
        if not item_keys:
            name_str = "(Empty)"
            left_arrow = "  "
            right_arrow = "  "
        else:
            self.item_idx = max(0, min(self.item_idx, len(item_keys) - 1))
            key = item_keys[self.item_idx]
            name_str = PASSIVE_OBJECTS[key]["name"] if key in PASSIVE_OBJECTS else key

            left_arrow = "< " if self.item_idx > 0 else "  "
            right_arrow = " >" if self.item_idx < len(item_keys) - 1 else "  "
        
        item_lbl = font.render(f"{left_arrow}{name_str}{right_arrow}", True, c_color)
        surface.blit(item_lbl, (16, 85))

        # Zone 1
        any_equipped = any(
            len(self.inventory.equipped_keys_for(i)) > 0 
            for i in range(len(self.party.members))
        )
        
        q_color = (240, 220, 50) if self.focus == "items" and self.active_zone == 1 else (150, 150, 150)
        if not any_equipped:
            q_color = (80, 80, 80)
            
        quitar_lbl = font.render("[ Remove Item ]", True, q_color)
        surface.blit(quitar_lbl, (16, 130))

        # Zone 3
        b_color = (240, 220, 50) if self.focus == "items" and self.active_zone == 2 else (150, 150, 150)
        back_lbl = font.render("[ Back ]", True, b_color)
        surface.blit(back_lbl, (16, 175))

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
            if self.isUnequipping:
                header_str = "Remove item to: "
            else:
                item_name = ""
                if self.selectedItemKey and self.selectedItemKey in PASSIVE_OBJECTS:
                    item_name = PASSIVE_OBJECTS[self.selectedItemKey]["name"]
                header_str = f"Equipped {item_name}:" if item_name else "give to: "
                
            header_lbl = medium.render(header_str, True, (240, 220, 50))
            surface.blit(header_lbl, (panelX + 10, panelY + 10))

            pygame.draw.line(surface, (40, 40, 60), (panelX + 10, panelY + 34), (panelX + panelW - 10, panelY + 34))

            if self.membersMenu:
                self.membersMenu.render(surface)
        else:
            item_keys = self.inventory.all_keys()
            if not item_keys or self.item_idx >= len(item_keys):
                return

            key = item_keys[self.item_idx]
            if key not in PASSIVE_OBJECTS:
                return
                
            objDef = PASSIVE_OBJECTS[key]
         
            iconSize = 32
            # Asegúrate de que icon_surface recibe los parámetros correctos según tu implementación
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
