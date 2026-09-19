
from gale.state import BaseState
from gale.input_handler import InputData

import settings

class GameOverState(BaseState):
    def enter(self, *args, **kwargs):
        settings.stop_music("battle")
        
    def on_input(self, input_id, input_data):
        if input_id == "enter" and input_data.pressed:
            self.state_machine.clear()
            settings.stop_music("battle")
            from src.States.Game.StartState import StartState
            self.state_machine.push(StartState(self.state_machine))


    def render(self, surface):
        surface.fill((0, 0, 0))
        
        medium = settings.FONTS["medium"]
        title = medium.render("Game Over", True, (240, 220, 50))
        titleRect = title.get_rect(center = (settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 ))
        surface.blit(title, titleRect)

        small = settings.FONTS["small"]
        hint = small.render("Press Enter to return to the menu", True, (200, 200, 200))
        hintRect = hint.get_rect(center=(settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 + 24))
        surface.blit(hint, hintRect)

        


        
        
