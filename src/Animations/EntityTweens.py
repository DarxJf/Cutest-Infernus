from typing import Callable, Any

from gale.timer import Timer

import settings


class EntityTweens:
    @staticmethod
    def slide_to(
        entity: Any, 
        dest_x: int, 
        dest_y: int, 
        duration: float = 0.3, 
        on_finish: Callable = None
    ) -> None:
        
        target_pixel_x = dest_x * settings.TILE_SIZE
        target_pixel_y = dest_y * settings.TILE_SIZE
        
        # Wrapped in a list of tuples: [(object, {attributes})]
        # Added "in_out_quad" for a smooth acceleration and deceleration
        Timer.tween(
            duration,
            [(entity, {"x": target_pixel_x, "y": target_pixel_y})],
            ease_function_name="in_out_quad",
            on_finish=on_finish
        )

    @staticmethod
    def bump_to(
        entity: Any, 
        target_x: int, 
        target_y: int, 
        duration: float = 0.2, 
        on_finish: Callable = None
    ) -> None:
        
        orig_pixel_x = entity.x
        orig_pixel_y = entity.y
        
        dx = target_x - entity.mapX
        dy = target_y - entity.mapY
        
        dir_x = max(-1, min(1, dx))
        dir_y = max(-1, min(1, dy))
        
        bump_pixel_x = orig_pixel_x + (dir_x * (settings.TILE_SIZE // 3))
        bump_pixel_y = orig_pixel_y + (dir_y * (settings.TILE_SIZE // 3))
        
        def go_back():
            Timer.tween(
                duration / 2,
                [(entity, {"x": orig_pixel_x, "y": orig_pixel_y})],
                ease_function_name="in_quad",
                on_finish=on_finish
            )
            
        Timer.tween(
            duration / 2,
            [(entity, {"x": bump_pixel_x, "y": bump_pixel_y})],
            ease_function_name="out_cubic",
            on_finish=go_back
        )
