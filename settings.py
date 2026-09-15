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

VIRTUAL_WIDTH = 540
VIRTUAL_HEIGHT = 260

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
    "menu_bg": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "menu_bg.png"),
   
    "cursors": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "cursors.png"),
    **{
        f"room_{p}": pygame.image.load(
            BASE_DIR / "assets"/ "Sprites" / "Rooms" / f"room_{p}.png"
        )
        for p in ROOM_PALETTES
    },

    "rock": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Objects" / "rock.png"),
    "floor_torch": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Objects" / "floor_torch.png"),
    "object_icons": pygame.image.load(BASE_DIR/ "assets"/"Sprites"/"Objects"/"objects.png"),
    "action_icons":pygame.image.load(BASE_DIR/ "assets"/"Sprites"/"Objects"/"action_icons.png"),

    "cloud_walk": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Entities" / "Characters" / "cloud_walk.png"),
    "pelusa_walk": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Entities" / "Characters" / "pelusa_walk.png"),
    "chloe_walk": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Entities" / "Characters" / "chloe_walk.png"),
    "balthazar_walk": pygame.image.load(BASE_DIR / "assets" / "Sprites" / "Entities" / "Characters" / "balthazar_walk.png"),
   
    "slime-down": pygame.image.load(BASE_DIR/ "assets"/ "Sprites" /"Entities"/"Enemies"/"Slime"/"Slime_pink_down.png"),
    "slime-up": pygame.image.load(BASE_DIR/ "assets" /"Sprites" /"Entities" /"Enemies"/ "Slime" /"Slime_pink_up.png"),
    "skel-idle-down": pygame.image.load(BASE_DIR /"assets"/"Sprites"/"Entities"/"Enemies"/"Skeleton"/"Idle"/"Skel_idle_down.png"),
    "skel-idle-left":pygame.image.load(BASE_DIR /"assets"/"Sprites"/"Entities"/"Enemies"/"Skeleton"/"Idle"/"Skel_idle_left.png"),
    "skel-idle-right": pygame.image.load(BASE_DIR / "assets"/"Sprites"/"Entities"/"Enemies"/"Skeleton"/"Idle"/"Skel_idle_right.png"),
    "skel-idle-up": pygame.image.load(BASE_DIR/"assets"/"Sprites"/"Entities"/"Enemies"/"Skeleton"/"Idle"/"Skel_idle_up.png"),
    "skel-walk-down":pygame.image.load(BASE_DIR/ "assets"/"Sprites"/"Entities"/"Enemies"/"Skeleton"/"Walk"/"Skel_walk_down.png"),
    "skel-walk-left":pygame.image.load(BASE_DIR / "assets"/"Sprites"/"Entities"/"Enemies"/"Skeleton"/"Walk"/"Skel_walk_left.png"),
    "skel-walk-right":pygame.image.load(BASE_DIR /"assets"/"Sprites"/"Entities"/"Enemies"/"Skeleton"/"Walk"/"Skel_walk_right.png"),
    "skel-walk-up":pygame.image.load(BASE_DIR /"assets"/"Sprites"/"Entities"/"Enemies"/"Skeleton"/"Walk"/"Skel_walk_up.png"),
    "demon-idle-down":pygame.image.load(BASE_DIR /"assets"/"Sprites"/"Entities"/"Enemies"/"Demon"/"Idle"/"Zombie_idle_down.png"),
    "demon-idle-left":pygame.image.load(BASE_DIR /"assets"/"Sprites"/"Entities"/"Enemies"/"Demon"/"Idle"/"Zombie_idle_left.png"),
    "demon-idle-right":pygame.image.load(BASE_DIR /"assets"/"Sprites"/"Entities"/"Enemies"/"Demon"/"Idle"/"Zombie_idle_right.png"),
    "demon-idle-up":pygame.image.load(BASE_DIR /"assets"/"Sprites"/"Entities"/"Enemies"/"Demon"/"Idle"/"Zombie_idle_up.png"),
    "demon-walk-down":pygame.image.load(BASE_DIR/"assets"/"Sprites"/"Entities"/"Enemies"/"Demon"/"Walk"/"Zombie_walk_down.png"),
    "demon-walk-left":pygame.image.load(BASE_DIR/"assets"/"Sprites"/"Entities"/"Enemies"/"Demon"/"Walk"/"Zombie_walk_left.png"),
    "demon-walk-right":pygame.image.load(BASE_DIR/"assets"/"Sprites"/"Entities"/"Enemies"/"Demon"/"Walk"/"Zombie_walk_right.png"),
    "demon-walk-up": pygame.image.load(BASE_DIR/"assets"/"Sprites"/"Entities"/"Enemies"/"Demon"/"Walk"/"Zombie_walk_up.png"),
}

FRAMES = {
    "cursors": frames.generate_frames(TEXTURES["cursors"], 16, 16),
     **{
        f"room_{p}": frames.generate_frames(TEXTURES[f"room_{p}"], 16, 16)
        for p in ROOM_PALETTES
    },

    "rock": frames.generate_frames(TEXTURES["rock"], 15, 15),
    "floor_torch": frames.generate_frames(TEXTURES["floor_torch"], 16, 32),
    "object_icons": frames.generate_frames(TEXTURES["object_icons"], 16, 16),
    "action_icons": frames.generate_frames(TEXTURES["action_icons"], 16, 16),

    "cloud_walk": frames.generate_frames(TEXTURES["cloud_walk"], 25, 24),
    "pelusa_walk": frames.generate_frames(TEXTURES["pelusa_walk"], 25, 24),
    "chloe_walk": frames.generate_frames(TEXTURES["chloe_walk"], 25, 24),
    "balthazar_walk": frames.generate_frames(TEXTURES["balthazar_walk"], 25, 24),
    "slime-down":frames.generate_frames(TEXTURES["slime-down"], 13, 14),
    "slime-up":frames.generate_frames(TEXTURES["slime-up"], 13, 14),
    "skel-idle-down": frames.generate_frames(TEXTURES["skel-idle-down"], 16, 16),
    "skel-idle-left": frames.generate_frames(TEXTURES["skel-idle-left"], 16, 16),
    "skel-idle-right":frames.generate_frames(TEXTURES["skel-idle-right"], 16, 16),
    "skel-idle-up":frames.generate_frames(TEXTURES["skel-idle-right"], 16, 16),
    "skel-walk-down":frames.generate_frames(TEXTURES[ "skel-walk-down"], 16, 17),
    "skel-walk-left":frames.generate_frames(TEXTURES["skel-walk-left"], 16, 17),
    "skel-walk-right":frames.generate_frames(TEXTURES[ "skel-walk-right"], 16, 17),
    "skel-walk-up":frames.generate_frames(TEXTURES["skel-walk-up"], 16, 17),
    "demon-idle-down":frames.generate_frames(TEXTURES["demon-idle-down"], 16, 16),
    "demon-idle-left":frames.generate_frames(TEXTURES["demon-idle-left"], 16, 16),
    "demon-idle-right":frames.generate_frames(TEXTURES[ "demon-idle-right"], 16, 16),
    "demon-idle-up":frames.generate_frames(TEXTURES["demon-idle-up"], 16, 16),
    "demon-walk-down":frames.generate_frames(TEXTURES["demon-walk-down"], 16, 17),
    "demon-walk-left":frames.generate_frames(TEXTURES["demon-walk-left"], 16, 17),
    "demon-walk-right":frames.generate_frames(TEXTURES["demon-walk-right"], 16, 17),
    "demon-walk-up":frames.generate_frames(TEXTURES[ "demon-walk-up"], 16, 17),
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