"""
Submenu: view and modify the action slots of each party member.

Two-stage flow:
    1. Pick a member.
    2. Pick a slot to replace, then pick a new action from the pool.
"""
# Arreglado batle

from typing import Any, List

import pygame

from gale.state import BaseState

import settings
from src.Gui.ActionInfoPanel import ActionInfoPanel
from src.Models.ActionCards import Action
from src.Definitions.ActionCards import (
    UNIVERSAL_ACTIONS,
    WARRIOR_ACTIONS, ROGUE_ACTIONS, FAIRY_ACTIONS, MAGE_ACTIONS,
)

CLASS_ACTIONS = {
    "Warrior": WARRIOR_ACTIONS,
    "Rogue":   ROGUE_ACTIONS,
    "Fairy":   FAIRY_ACTIONS,
    "Mage":    MAGE_ACTIONS,
}

class ManageActionsState(BaseState):
    def enter(self, runState: Any, onClose=None) -> None:
        self.party = runState.party
        self.onClose = onClose or (lambda: None)

        self.stage = "member"          
        
        self.memberIdx = 0
        self.modeIdx = 0    
        self.slotIdx = 0
        self.poolIdx = 0
        self.scrollOffset = 0 
        
        self.errorMessage = ""
        self.errorTimer = 0.0

        self.showActionInfo: bool = False

    def _get_action_def(self, member: Any, key: str) -> dict:
        classPool = CLASS_ACTIONS.get(member.classType, {})
        if key in classPool:
            return classPool[key]
            
        if key in UNIVERSAL_ACTIONS:
            return UNIVERSAL_ACTIONS[key]
            
        return None

    def _get_available_pool(self) -> List[str]:
        member = self.party.members[self.memberIdx]
        classPool = CLASS_ACTIONS.get(member.classType, {})
        
        pool = {**UNIVERSAL_ACTIONS, **classPool}
        
        # Avoid duplicates
        equipped_keys = [act.key for act in member.actionSlots if hasattr(act, 'key')]

        return [key for key in pool.keys() if key not in equipped_keys]

    def update(self, dt: float) -> None:
        if self.errorTimer > 0:
            self.errorTimer -= dt

    def on_input(self, inputId: str, inputData: Any) -> None:
        if not inputData.pressed:
            return

        if getattr(self, "showActionInfo", False):
            if inputId in ["undo", "info",]:
                self.showActionInfo = False
                if "select" in settings.SOUNDS: settings.SOUNDS["select"].play()
            return

        if inputId == "info":
            member = self.party.members[self.memberIdx]
            if self.stage == "add":
                if self._get_available_pool():
                    self.showActionInfo = True
                    if "select" in settings.SOUNDS: settings.SOUNDS["select"].play()
            elif self.stage == "remove":
                if member.actionSlots:
                    self.showActionInfo = True
                    if "select" in settings.SOUNDS: settings.SOUNDS["select"].play()
            return

        if self.stage == "member":
            if inputId == "moveLeft":
                self.memberIdx = max(0, self.memberIdx - 1)
                settings.SOUNDS["select"].play()
            elif inputId == "moveRight":
                self.memberIdx = min(len(self.party.members) - 1, self.memberIdx + 1)
                settings.SOUNDS["select"].play()
            elif inputId == "enter":
                settings.SOUNDS["select"].play()
                self.stage = "mode"
            elif inputId == "undo":
                self.state_machine.pop()
                self.onClose()

        elif self.stage == "mode":
            if inputId == "moveLeft":
                self.modeIdx = 0
                settings.SOUNDS["select"].play()
            elif inputId == "moveRight":
                self.modeIdx = 1
                settings.SOUNDS["select"].play()
            elif inputId == "enter":
                settings.SOUNDS["select"].play()
                if self.modeIdx == 0:
                    self.stage = "add"
                    self.poolIdx = 0
                else:
                    self.stage = "remove"
                    self.slotIdx = 0
            elif inputId == "undo":
                self.stage = "member"

        elif self.stage == "add":
            pool = self._get_available_pool()
            if inputId == "moveLeft":
                self.poolIdx = max(0, self.poolIdx - 1)
                if self.poolIdx < self.scrollOffset:
                    self.scrollOffset = self.poolIdx
                settings.SOUNDS["select"].play()
            elif inputId == "moveRight":
                self.poolIdx = min(len(pool) - 1, self.poolIdx + 1)
                if self.poolIdx >= self.scrollOffset + 5: 
                    self.scrollOffset += 1
                settings.SOUNDS["select"].play()
            elif inputId == "enter":
                member = self.party.members[self.memberIdx]
                max_slots = getattr(member, 'slotActions', 4) 
                
                if len(member.actionSlots) >= max_slots:
                    self.errorMessage = "¡Slots Llenos!"
                    self.errorTimer = 2.0
                    if "error" in settings.SOUNDS: settings.SOUNDS["error"].play()
                elif pool:
                    selected_key = pool[self.poolIdx]
                    action_def = self._get_action_def(member, selected_key)
                    new_action = Action(selected_key, action_def)
                    
                    member.actionSlots.append(new_action)
                    settings.SOUNDS["select"].play()
                    self.poolIdx = max(0, min(self.poolIdx, len(self._get_available_pool()) - 1))
            elif inputId == "undo":
                self.stage = "mode"

        elif self.stage == "remove":
            member = self.party.members[self.memberIdx]
            if inputId == "moveLeft":
                self.slotIdx = max(0, self.slotIdx - 1)
                settings.SOUNDS["select"].play()
            elif inputId == "moveRight":
                self.slotIdx = min(len(member.actionSlots) - 1, self.slotIdx + 1)
                settings.SOUNDS["select"].play()
            elif inputId == "enter":
                if member.actionSlots:
                    member.actionSlots.pop(self.slotIdx)
                    settings.SOUNDS["select"].play()
                    self.slotIdx = max(0, min(self.slotIdx, len(member.actionSlots) - 1))
            elif inputId == "undo":
                self.stage = "mode"

    def _draw_icon(self, surface: pygame.Surface, action_def: dict, x: int, y: int) -> None:
        if not action_def:
            return
            
        texture_id = action_def.get("texture_id")
        frame_index = action_def.get("frame_index")
        
        if texture_id and frame_index is not None and texture_id in settings.TEXTURES and texture_id in settings.FRAMES:
            icon_surface = settings.TEXTURES[texture_id]

            frame_rect = settings.FRAMES[texture_id][frame_index]

            surface.blit(icon_surface, (x, y), area=frame_rect)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((15, 15, 22))
        font = settings.FONTS["small"]

        start_x = settings.VIRTUAL_WIDTH // 2 - (len(self.party.members) * 50) // 2
        for i, member in enumerate(self.party.members):
            color = (240, 220, 50) if self.stage == "member" and i == self.memberIdx else (100, 100, 100)
            txt = font.render(member.name, True, color)
            surface.blit(txt, (start_x + i * 50, 20))

        if self.stage == "member":
            return 

        add_color = (240, 220, 50) if self.stage == "mode" and self.modeIdx == 0 else (150, 150, 150)
        rem_color = (240, 220, 50) if self.stage == "mode" and self.modeIdx == 1 else (150, 150, 150)
        
        surface.blit(font.render("[ ADD ]", True, add_color), (settings.VIRTUAL_WIDTH // 2 - 80, 30))
        surface.blit(font.render("[ REMOVE ]", True, rem_color), (settings.VIRTUAL_WIDTH // 2 + 10, 30))

        member = self.party.members[self.memberIdx]

        # Slots
        surface.blit(font.render("Equipped Slots:", True, (200, 200, 200)), (20, 50))
        for i, action_obj in enumerate(member.actionSlots):
            x_pos = 20 + (i * 60)
            rect = pygame.Rect(x_pos, 80, 55, 70)
            b_color = (255, 100, 100) if self.stage == "remove" and i == self.slotIdx else (100, 100, 100)
            
            pygame.draw.rect(surface, (40, 30, 40), rect, border_radius=4)
            pygame.draw.rect(surface, b_color, rect, width=2, border_radius=4)

            act_key = getattr(action_obj, 'key', action_obj.name) 
            adef = self._get_action_def(member, act_key)
            
            self._draw_icon(surface, adef, x_pos + 20, 85)
            
            name = adef["name"][:7] if adef else action_obj.name[:7]
            txt = font.render(name, True, (255, 255, 255))
            surface.blit(txt, (x_pos + 10, 120))

        surface.blit(font.render("Actions Pool:", True, (200, 200, 200)), (20, 160))
        pool = self._get_available_pool()
        
        visible_pool = pool[self.scrollOffset : self.scrollOffset + 5]
        for i, act_key in enumerate(visible_pool):
            actual_idx = i + self.scrollOffset
            x_pos = 20 + (i * 60)
            rect = pygame.Rect(x_pos, 190, 55, 70)
            b_color = (100, 255, 100) if self.stage == "add" and actual_idx == self.poolIdx else (100, 100, 100)
            
            pygame.draw.rect(surface, (30, 40, 60), rect, border_radius=4)
            pygame.draw.rect(surface, b_color, rect, width=2, border_radius=4)
            
            adef = self._get_action_def(member, act_key)

            self._draw_icon(surface, adef, x_pos + 20, 195)
            
            name = adef["name"][:7] if adef else act_key[:7]
            txt = font.render(name, True, (255, 255, 255))
            surface.blit(txt, (x_pos + 10, 230))

        if self.errorTimer > 0:
            err_txt = settings.FONTS["medium"].render(self.errorMessage, True, (255, 50, 50))
            surface.blit(err_txt, err_txt.get_rect(center=(settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT - 20)))

        if getattr(self, "showActionInfo", False):
            member = self.party.members[self.memberIdx]
            selected_action = None

            if self.stage == "add":
                pool = self._get_available_pool()
                if pool and self.poolIdx < len(pool):
                    act_key = pool[self.poolIdx]
                    adef = self._get_action_def(member, act_key)
                    selected_action = Action(act_key, adef)
            elif self.stage == "remove":
                if member.actionSlots and self.slotIdx < len(member.actionSlots):
                    selected_action = member.actionSlots[self.slotIdx]

            if selected_action:
                panel_x = settings.VIRTUAL_WIDTH - 240 - 16
                panel_y = (settings.VIRTUAL_HEIGHT // 2) - 80
                ActionInfoPanel.render(surface, selected_action, panel_x, panel_y)
