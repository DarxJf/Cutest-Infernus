"""
This file contains all CONSTANTS and manage of MUSIC,
Sound and Fonts of the game. Alse input_handlers.
"""

import pathlib
import pygame

from gale import input_handler
from gale import frames

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "moveLeft")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "moveRight")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_UP, "moveUp")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_DOWN, "moveDown")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_KP_ENTER, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_p, "pause")

TITLE = "Cutest Inferno"

BASE_DIR = pathlib.Path(__file__).parent

SAVE_DIR = BASE_DIR / "saves"
SAVE_SLOTS = ["slot1", "slot2", "slot3"]

VIRTUAL_WIDTH = 384
VIRTUAL_HEIGHT = 224

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "Fonts" / "BoldPixels.ttf", 12),
    "medium": pygame.font.Font(BASE_DIR / "assets"/ "Fonts" / "BoldPixels.ttf", 16 ),
    "large": pygame.font.Font(BASE_DIR / "assets"/ "Fonts" / "BoldPixels.ttf", 24)   
}

TEXTURES = {
    "cursors": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "cursors.png")
}

FRAMES = {
    "cursors": frames.generate_frames(TEXTURES["cursors"], 16, 16)
}

TILE_IDS = {
    "cursorRight": 61,
    "arrowRight":133,
    "arrowLeft": 132,
}

SOUNDS = {
    "select": pygame.mixer.Sound(BASE_DIR / "assets" / "Music" / "select.wav" )
}