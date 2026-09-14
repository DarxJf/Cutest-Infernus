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
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SPACE, "space")

TITLE = "Cutest Inferno"

BASE_DIR = pathlib.Path(__file__).parent

SAVE_DIR = BASE_DIR / "saves"
SAVE_SLOTS = ["slot1", "slot2", "slot3"]

VIRTUAL_WIDTH = 384
VIRTUAL_HEIGHT = 224

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

TILE_SIZE = 16

FONTS = {
    "small": pygame.font.Font(BASE_DIR / "assets" / "Fonts" / "BoldPixels.ttf", 12),
    "medium": pygame.font.Font(BASE_DIR / "assets"/ "Fonts" / "BoldPixels.ttf", 16 ),
    "large": pygame.font.Font(BASE_DIR / "assets"/ "Fonts" / "BoldPixels.ttf", 24)   
}

ROOM_PALETTES = ["blue", "red", "green", "brown", "gray"]

TEXTURES = {
    "cursors": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "cursors.png"),
    **{
        f"room_{p}": pygame.image.load(
            BASE_DIR / "assets"/ "Sprites" / "Rooms" / f"room_{p}.png"
        )
        for p in ROOM_PALETTES
    },
    "rock": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Objects" / "rock.png"),
    "floor_torch": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Objects" / "floor_torch.png"),
    "cloud_walk": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Entities" / "Characters" / "cloud_walk.png"),
    "pelusa_walk": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Entities" / "Characters" / "pelusa_walk.png"),
    "chloe_walk": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Entities" / "Characters" / "chloe_walk.png"),
    "balthazar_walk": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Entities" / "Characters" / "balthazar_walk.png"),
    "menu_bg": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "menu_bg.png"),
}

FRAMES = {
    "cursors": frames.generate_frames(TEXTURES["cursors"], 16, 16),
     **{
        f"room_{p}": frames.generate_frames(TEXTURES[f"room_{p}"], 16, 16)
        for p in ROOM_PALETTES
    },
    "rock": frames.generate_frames(TEXTURES["rock"], 15, 15),
    "floor_torch": frames.generate_frames(TEXTURES["floor_torch"], 16, 32),
    "cloud_walk": frames.generate_frames(TEXTURES["cloud_walk"], 25, 24),
    "pelusa_walk": frames.generate_frames(TEXTURES["pelusa_walk"], 25, 24),
    "chloe_walk": frames.generate_frames(TEXTURES["chloe_walk"], 25, 24),
    "balthazar_walk": frames.generate_frames(TEXTURES["balthazar_walk"], 25, 24),
}

TILE_IDS = {
  
    "floor": 1,

    "wallTopLeftCorner":  13,
    "wallTopRightCorner": 17,
  
    "wallTopOuterLeft":  14,
    "wallTopOuterMid":   15,
    "wallTopOuterRight": 16,
 
    "wallTopInnerLeft":  27,
    "wallTopInnerMid":   28,
    "wallTopInnerRight": 29,

    "wallLeftTop":    26,
    "wallLeftMid":    39, 
    "wallLeftBottom": 52,
  
    "wallRightTop":    30,
    "wallRightMid":    43,
    "wallRightBottom": 56,
   
    "wallBottomLeftUpper": 65,
    "wallBottomLeftLower": 78,
    "wallBottomRightUpper": 69,
    "wallBottomRightLower": 82,

    "wallBottomOuterLeft":  66,
    "wallBottomOuterMid":   67,
    "wallBottomOuterRight": 68,
   
    "wallBottomInnerLeft":  79,
    "wallBottomInnerMid":   80,
    "wallBottomInnerRight": 81,

    "doorTopFrames":    [19, 20, 21, 32, 33, 34],
    "doorLeftFrames":   [44, 45, 57, 58, 70, 71],
    "doorBottomFrames": [84, 85, 86, 97, 98, 99],
    "doorRightFrames":  [47, 48, 60, 61, 73, 74],
    "doorOpenFrames":   [87, 88, 89, 100, 101, 102],
    
    "cursorRight": 61,
    "arrowRight":133,
    "arrowLeft": 132,
    
}

SOUNDS = {
    "select": pygame.mixer.Sound(BASE_DIR / "assets" / "Music" / "select.wav" )
}