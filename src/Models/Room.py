import random
import pygame
import settings
from typing import Set, Tuple

from src.Definitions.Scenery import SCENERY

WALKABLE = 0
WALL = 1
WALL_TOP_ROWS = 2
WALL_BOTTOM_ROWS = 2
OBSTACLE = 2


class Room():
    def __init__(self, cols: int = 16, rows: int = 10) -> None:
        self.cols = cols
        self.rows = rows
        
        self.palette = random.choice(settings.ROOM_PALETTES)
        self.textureKey = f"room_{self.palette}"
        
        self.offsetX = (settings.VIRTUAL_WIDTH - (self.cols * settings.TILE_SIZE)) // 2
        self.offsetY = (settings.VIRTUAL_HEIGHT - (self.rows * settings.TILE_SIZE)) // 2
        
        self.logicalGrid = []
        self.visualGrid = []
        self.doors = []

        self.beigeCells: Set[Tuple[int, int]] = set()
       

        self.doorSurfaces = {
            "top":    self._build_door_surface(settings.TILE_IDS["doorTopFrames"],    3, 2),
            "left":   self._build_door_surface(settings.TILE_IDS["doorLeftFrames"],   2, 3),
            "bottom": self._build_door_surface(settings.TILE_IDS["doorBottomFrames"], 3, 2),
            "right":  self._build_door_surface(settings.TILE_IDS["doorRightFrames"],  2, 3),
            "open":   self._build_door_surface(settings.TILE_IDS["doorOpenFrames"],   3, 2),
        }
        
        self._generate_logical_grid()
        self._generate_visual_grid()
        self._place_doors()
        self._place_objects()
     

    def _generate_logical_grid(self) -> None:
        self.logicalGrid = [[WALKABLE for _ in range(self.cols)] for _ in range(self.rows)]

        topWallEnd = WALL_TOP_ROWS - 1             
        bottomWallStart = self.rows - WALL_BOTTOM_ROWS
        
        for y in range(self.rows):
            for x in range(self.cols):
                if x == 0 or x == self.cols - 1 or y <= topWallEnd or y >= bottomWallStart:
                    self.logicalGrid[y][x] = WALL


    def _generate_visual_grid(self) -> None:
        self.visualGrid = [[settings.TILE_IDS["floor"] for _ in range(self.cols)] for _ in range(self.rows)]

        topWallEnd = WALL_TOP_ROWS - 1
        bottomWallStart = self.rows - WALL_BOTTOM_ROWS

        for y in range(self.rows):
            for x in range(self.cols):

                if self.logicalGrid[y][x] == WALKABLE:
                    if (x + y) % 2 == 1:
                        self.beigeCells.add((x,y))

                val = self.logicalGrid[y][x]
                if val == WALL:
                    if y == 0:
                        if x == 0: tileID = settings.TILE_IDS["wallTopLeftCorner"]
                        elif x == self.cols - 1: tileID = settings.TILE_IDS["wallTopRightCorner"]
                        else: tileID = settings.TILE_IDS["wallTopOuterMid"]
                    elif y == 1:
                        if x == 0: tileID = settings.TILE_IDS["wallLeftTop"]
                        elif x == self.cols - 1: tileID = settings.TILE_IDS["wallRightTop"]
                        else: tileID = settings.TILE_IDS["wallTopInnerMid"]
                        
                    elif y == bottomWallStart:
           
                        if x == 0: tileID = settings.TILE_IDS["wallBottomLeftUpper"]
                        elif x == self.cols - 1: tileID = settings.TILE_IDS["wallBottomRightUpper"]
                        else: tileID = settings.TILE_IDS["wallBottomOuterMid"] 
                    elif y == bottomWallStart + 1:
                        if x == 0: tileID = settings.TILE_IDS["wallBottomLeftLower"]
                        elif x == self.cols - 1: tileID = settings.TILE_IDS["wallBottomRightLower"]
                        else: tileID = settings.TILE_IDS["wallBottomInnerMid"] 
                        
                    else:
                        if x == 0:
                            if y == bottomWallStart - 1:
                                tileID = settings.TILE_IDS["wallLeftBottom"]
                            else:
                                tileID = settings.TILE_IDS["wallLeftMid"]
                                
                        elif x == self.cols - 1:
                            if y == bottomWallStart - 1:
                                tileID = settings.TILE_IDS["wallRightBottom"]
                            else:
                                tileID = settings.TILE_IDS["wallRightMid"]
                        else:
                            tileID = settings.TILE_IDS["floor"]
                            
                    self.visualGrid[y][x] = tileID

    def _place_doors(self) -> None:
        doorTopX = (self.cols - 3) // 2
        self.doors.append((doorTopX, 0, "top"))

        self.doors.append((doorTopX, self.rows - 2, "bottom"))

        doorLeftY = (self.rows - 3) // 2
        self.doors.append((0, doorLeftY, "left"))

        self.doors.append((self.cols - 2, doorLeftY, "right"))

    def _build_door_surface(self, frameIndices: list, cols: int, rows: int) -> pygame.Surface:
        texture = settings.TEXTURES[self.textureKey]
        frames = settings.FRAMES[self.textureKey]
        tile = settings.TILE_SIZE

        surface = pygame.Surface((cols * tile, rows * tile), pygame.SRCALPHA)

        for i, idx in enumerate(frameIndices):
            row = i // cols
            col = i % cols
            surface.blit(texture, (col * tile, row * tile), frames[idx])

        return surface

    def _place_objects(self) -> None:
            self.objects = []
            
            for _ in range(3): 
                rx = random.randint(2, (self.cols // 2) - 2)
                ry = random.randint(2, self.rows - 4)
                
                if self.logicalGrid[ry][rx] == WALKABLE:
                    self.objects.append({"x": rx, "y": ry, "def": SCENERY["rock"], "anim_timer": 0.0, "anim_frame": 0})
                    self.logicalGrid[ry][rx] = OBSTACLE
                    
                    mx = self.cols - 1 - rx
                    self.objects.append({"x": mx, "y": ry, "def": SCENERY["rock"], "anim_timer": 0.0, "anim_frame": 0})
                    self.logicalGrid[ry][mx] = OBSTACLE

            torchColors = ["torch_red", "torch_green", "torch_blue", "torch_purple"]
            roomTorchkey = random.choice(torchColors)
            
            doorTopX = (self.cols - 3) // 2
            
            self.objects.append({
                "x": doorTopX - 1, 
                "y": 1, 
                "def": SCENERY[roomTorchkey],
                "anim_timer": 0.0,
                "anim_frame": 0
            })
            
            self.objects.append({
                "x": doorTopX + 3, 
                "y": 1, 
                "def": SCENERY[roomTorchkey],
                "anim_timer": 0.0,
                "anim_frame": 0
            })

    def update(self, dt: float) -> None:
        for obj in self.objects:
            objDef = obj["def"]        
            if "animation" in objDef:
                obj["anim_timer"] += dt
                if obj["anim_timer"] >= objDef["animation_interval"]:
                    obj["anim_timer"] = 0.0
                    obj["anim_frame"] = (obj["anim_frame"] + 1) % len(objDef["animation"])
   
    def render(self, surface: pygame.Surface) -> None:
        texture = settings.TEXTURES[self.textureKey]
        frames = settings.FRAMES[self.textureKey]
        tile = settings.TILE_SIZE

        beigeTexture = settings.TEXTURES["tile-set"]
        beigeFrames = settings.FRAMES["tile-set"]
        beigeFrames = beigeFrames[settings.TILE_IDS["floor-beige"]]
        
        for y in range(self.rows):
            for x in range(self.cols):  
                px = self.offsetX + (x * settings.TILE_SIZE)
                py = self.offsetY + (y * settings.TILE_SIZE)

                if (x,y) in self.beigeCells:
                    surface.blit(beigeTexture, (px,py), beigeFrames)
                else:
                    tileID = self.visualGrid[y][x]
                    surface.blit(texture, (px, py), frames[tileID])
        

        for (x, y, kind) in self.doors:
            surface.blit(
                self.doorSurfaces[kind],
                (self.offsetX + x * tile, self.offsetY + y * tile),
            )

        for obj in self.objects:
            objDef = obj["def"]
            texId = objDef["texture_id"]
        
            if "animation" in objDef:
                frameList = objDef["animation"]
                actualFrameIdx = frameList[obj["anim_frame"]]
            else:
                actualFrameIdx = objDef["frame_index"]
            
            texture = settings.TEXTURES[texId]
            frames = settings.FRAMES[texId]
            
            px = self.offsetX + (obj["x"] * settings.TILE_SIZE)
            py = self.offsetY + (obj["y"] * settings.TILE_SIZE)
            
            frameRect = frames[actualFrameIdx]
         
            surface.blit(texture, (px, py - (frameRect.height - settings.TILE_SIZE)), frameRect)

    def is_walkable(self, x: int, y: int) -> bool:
        if 0 > x or x >= self.cols or 0 > y or y >= self.rows:
            return False
        else:
            return self.logicalGrid[y][x] == WALKABLE
    