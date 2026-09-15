"""
Submenu: view and modify the action slots of each party member.

Two-stage flow:
    1. Pick a member.
    2. Pick a slot to replace, then pick a new action from the pool.
"""
# POR ARREGLAR

from typing import Any

import pygame

from gale.state import BaseState

import settings
from src.Gui.Menu import Menu
from src.Models.Party import Party
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
    def enter(self, runState, onClose=None) -> None:
        self.party = runState.party
        self.onClose = onClose or (lambda: None)

        self.stage = "member"          # "member" | "slot" | "action"
        self.selectedMemberIdx: int = None
        self.selectedSlotIdx: int = None

        self._build_member_menu()

    # ------------------------------------------------------------------ #

    def _build_member_menu(self) -> None:
        items = []
        for i, member in enumerate(self.party.members):
            items.append((member.classType, self._make_member_callback(i)))
        items.append(("Back", self._close))

        self.menu = Menu(
            settings.VIRTUAL_WIDTH / 2 - 80,
            settings.VIRTUAL_HEIGHT / 2 - 60,
            160,
            130,
            items=items,
            font=settings.FONTS["small"],
        )
        self.stage = "member"

    def _make_member_callback(self, index: int):
        def cb():
            self.selectedMemberIdx = index
            self._build_slot_menu()
        return cb

    def _build_slot_menu(self) -> None:
        member = self.party.members[self.selectedMemberIdx]
        items = []
        for slotIdx, actionKey in enumerate(member.actionSlots):
            actionDef = self._get_action_def(actionKey)
            name = actionDef["name"] if actionDef else actionKey
            items.append((f"Slot {slotIdx + 1}: {name}",
                          self._make_slot_callback(slotIdx)))
        items.append(("Cancel", self._cancel))

        self.menu = Menu(
            settings.VIRTUAL_WIDTH / 2 - 80,
            settings.VIRTUAL_HEIGHT / 2 - 60,
            160,
            130,
            items=items,
            font=settings.FONTS["small"],
        )
        self.stage = "slot"

    def _make_slot_callback(self, slotIdx: int):
        def cb():
            self.selectedSlotIdx = slotIdx
            self._build_action_menu()
        return cb

    def _build_action_menu(self) -> None:
        member = self.party.members[self.selectedMemberIdx]
        classPool = CLASS_ACTIONS.get(member.classType, {})

        pool = {**UNIVERSAL_ACTIONS, **classPool}

        items = []
        for actionKey, adef in pool.items():
            items.append((adef["name"], self._make_action_callback(actionKey)))
        items.append(("Cancel", self._cancel))

        self.menu = Menu(
            settings.VIRTUAL_WIDTH / 2 - 80,
            settings.VIRTUAL_HEIGHT / 2 - 60,
            160,
            130,
            items=items,
            font=settings.FONTS["small"],
        )
        self.stage = "action"

    def _make_action_callback(self, actionKey: str):
        def cb():
            member = self.party.members[self.selectedMemberIdx]
            member.actionSlots[self.selectedSlotIdx] = actionKey
            settings.SOUNDS["select"].play()
            self._build_slot_menu()
        return cb

    def _cancel(self) -> None:
        if self.stage == "slot":
            self._build_member_menu()
        elif self.stage == "action":
            self._build_slot_menu()

    def _close(self) -> None:
        self.state_machine.pop()
        self.onClose()

    # ------------------------------------------------------------------ #

    def _get_action_def(self, key: str):
        for pool in [UNIVERSAL_ACTIONS, *CLASS_ACTIONS.values()]:
            if key in pool:
                return pool[key]
        return None

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
            self._cancel()

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((15, 15, 22))

        medium = settings.FONTS["medium"]
        title = medium.render("Manage Actions", True, (240, 220, 50))
        surface.blit(title, title.get_rect(
            centerx=settings.VIRTUAL_WIDTH / 2, y=20,
        ))

        small = settings.FONTS["small"]

       
        hints = {
            "member": "Pick a member",
            "slot":   "Pick a slot to replace",
            "action": "Pick a new action",
        }
        hint = small.render(hints.get(self.stage, ""), True, (200, 200, 200))
        surface.blit(hint, hint.get_rect(
            centerx=settings.VIRTUAL_WIDTH / 2, y=44,
        ))

        self.menu.render(surface)