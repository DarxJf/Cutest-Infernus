from typing import Callable, Optional, Tuple

import pygame

from gale.state import BaseState
from gale.timer import Timer

import settings


class FadeOutState(BaseState):
    def enter(
        self,
        color: Tuple[int, int, int] = (255, 255, 255),
        time: float = 1,
        onComplete: Optional[Callable[[], None]] = None,
    ) -> None:
        self.color = color
        self.opacity = 255.0
        self.onComplete = onComplete or (lambda: None)
        Timer.tween(time, [(self, {"opacity": 0})], on_finish=self._finish_fade)

    def _finish_fade(self) -> None:
        self.state_machine.pop()
        self.onComplete()

    def render(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        overlay.fill(self.color)
        overlay.set_alpha(int(self.opacity))
        surface.blit(overlay, (0, 0))