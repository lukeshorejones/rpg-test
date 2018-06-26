# Map class
import math, pygame as pg, pytmx
from globals import *

class Map:
    def __init__(self, filename):
        tm  = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.matrix = [[0 for x in range(tm.width)] for y in range(tm.height)]
        self.blueSpawns = []
        self.redSpawns = []

    def render(self, surface):
        tileImage = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = tileImage(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmxdata.tilewidth, y*self.tmxdata.tileheight))
        for tile_object in self.tmxdata.objects:
            if tile_object.type == 'blueCamera':
                self.blueCameraSpawn = (tile_object.x, tile_object.y)
            if tile_object.type == 'redCamera':
                self.redCameraSpawn = (tile_object.x, tile_object.y)
            if tile_object.type == 'blueSpawn':
                self.blueSpawns.append((tile_object.x, tile_object.y))
            if tile_object.type == 'redSpawn':
                self.redSpawns.append((tile_object.x, tile_object.y))
            elif tile_object.type == 'obstacle':
                for i in range(int(tile_object.width/WIDTH)):
                    self.matrix[int(tile_object.y/HEIGHT)][int(tile_object.x/WIDTH) + i] = 2
                for i in range(int(tile_object.height/HEIGHT)):
                    self.matrix[int(tile_object.y/HEIGHT) + i][int(tile_object.x/WIDTH)] = 2

    def make_map(self):
        tempSurface = pg.Surface((self.width, self.height))
        self.render(tempSurface)
        return tempSurface

class BlueCamera:
    def __init__(self, g):
        if DISPLAY_WIDTH > g.gameMap.width:
            self.posx = -WIDTH*((DISPLAY_WIDTH - g.gameMap.width)//(2*WIDTH))
        else:
            self.posx = g.gameMap.blueCameraSpawn[0]
        if DISPLAY_HEIGHT > g.gameMap.height:
            self.posy = -HEIGHT*((DISPLAY_HEIGHT - g.gameMap.height)//(2*HEIGHT))
        else:
            self.posy = g.gameMap.blueCameraSpawn[1]

class RedCamera:
    def __init__(self, g):
        if DISPLAY_WIDTH > g.gameMap.width:
            self.posx = -WIDTH*((DISPLAY_WIDTH - g.gameMap.width)//(2*WIDTH))
        else:
            self.posx = g.gameMap.redCameraSpawn[0]
        if DISPLAY_HEIGHT > g.gameMap.height:
            self.posy = -HEIGHT*((DISPLAY_HEIGHT - g.gameMap.height)//(2*HEIGHT))
        else:
            self.posy = g.gameMap.redCameraSpawn[1]
