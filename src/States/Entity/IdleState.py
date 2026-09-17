from typing import Any

from gale.state import BaseState


class EntityIdleState(BaseState):
    def enter(self, entity: Any) -> None:
        self.entity = entity
        # Llama a la animación de reposo usando la memoria de dirección
        self.entity.change_animation(f"idle-{self.entity.facing}")
