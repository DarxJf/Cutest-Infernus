from typing import Any, Callable

from gale.state import BaseState

from src.Animations.EntityTweens import EntityTweens

class EntityWalkState(BaseState):
    def enter(self, entity: Any, targetX: int, targetY: int, callback: Callable = None) -> None:
        self.entity = entity
        self.callback = callback
        
        dx = targetX - self.entity.mapX
        dy = targetY - self.entity.mapY
        
        # Actualizamos la orientación basada en el vector de movimiento
        if abs(dx) > abs(dy):
            self.entity.facing = "right" if dx > 0 else "left"
        else:
            self.entity.facing = "down" if dy > 0 else "up"
            
        self.entity.change_animation(f"walk-{self.entity.facing}")
        
        # Actualizamos las coordenadas lógicas inmediatamente
        self.entity.mapX = targetX
        self.entity.mapY = targetY
        
        # Iniciamos el movimiento fluido
        EntityTweens.slide_to(
            self.entity, 
            targetX, 
            targetY, 
            duration=0.3, 
            on_finish=self.on_walk_finished
        )

    def on_walk_finished(self) -> None:
        # Al terminar el Tween, volvemos al estado de reposo y notificamos al sistema
        self.state_machine.change("idle", self.entity)
        if self.callback:
            self.callback()
