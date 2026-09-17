from typing import Any, Callable
from gale.state import BaseState
from src.Animations.EntityTweens import EntityTweens

class EntityAttackState(BaseState):
    def enter(self, entity: Any, targetX: int, targetY: int, callback: Callable = None) -> None:
        self.entity = entity
        self.callback = callback
        
        dx = targetX - self.entity.mapX
        dy = targetY - self.entity.mapY
        
        # Regla de prioridad para diagonales: Arriba/Abajo manda sobre los lados
        if dy < 0:
            self.entity.facing = "up"
        elif dy > 0:
            self.entity.facing = "down"
        elif dx > 0:
            self.entity.facing = "right"
        elif dx < 0:
            self.entity.facing = "left"
            
        self.entity.change_animation(f"attack-{self.entity.facing}")
        
        # Iniciamos el empuje visual del ataque
        EntityTweens.bump_to(
            self.entity, 
            targetX, 
            targetY, 
            duration=0.2, 
            on_finish=self.on_attack_finished
        )

    def on_attack_finished(self) -> None:
        self.state_machine.change("idle", self.entity)
        if self.callback:
            self.callback()
