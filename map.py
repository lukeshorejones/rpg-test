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
        self.blue_spawns = []
        self.red_spawns = []

    def render(self, surface):
        tileImage = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = tileImage(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmxdata.tilewidth, y*self.tmxdata.tileheight))
        for tile_object in self.tmxdata.objects:
            if tile_object.type == 'blue_cam':
                self.blue_cam_spawn = (tile_object.x, tile_object.y)
            if tile_object.type == 'red_cam':
                self.red_cam_spawn = (tile_object.x, tile_object.y)
            if tile_object.type == 'blue_spawn':
                self.blue_spawns.append((tile_object.x, tile_object.y))
            if tile_object.type == 'red_spawn':
                self.red_spawns.append((tile_object.x, tile_object.y))
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
        if DISPLAY_WIDTH > g.map.width:
            self.posx = -WIDTH*((DISPLAY_WIDTH - g.map.width)//(2*WIDTH))
        else:
            self.posx = g.map.blue_cam_spawn[0]
        if DISPLAY_HEIGHT > g.map.height:
            self.posy = -HEIGHT*((DISPLAY_HEIGHT - g.map.height)//(2*HEIGHT))
        else:
            self.posy = g.map.blue_cam_spawn[1]

class RedCamera:
    def __init__(self, g):
        if DISPLAY_WIDTH > g.map.width:
            self.posx = -WIDTH*((DISPLAY_WIDTH - g.map.width)//(2*WIDTH))
        else:
            self.posx = g.map.red_cam_spawn[0]
        if DISPLAY_HEIGHT > g.map.height:
            self.posy = -HEIGHT*((DISPLAY_HEIGHT - g.map.height)//(2*HEIGHT))
        else:
            self.posy = g.map.red_cam_spawn[1]
