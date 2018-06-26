# Sprite classes
import colorsys, copy, math, os, pygame as pg, shutil
from globals import *

class EndScreenDialogue(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((256, 128))
        self.image.fill(BLACK)
        self.image.set_alpha(204)

    def update(self, g):
        g.screen.blit(self.image, ((DISPLAY_WIDTH-256)/2, (DISPLAY_HEIGHT-128)/2))

class Fade(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.image.fill(BLACK)

    def start_fadeout(self, g):
        for i in range(16):
            g.clock.tick(FPS)
            self.image.set_alpha(i*16)

            g.screen.blit(g.startScreenMapImg, g.startScreenPos)
            g.screen.blit(g.startScreenImg, (0,0))
            g.titleText.update(g)
            for i in range(len(g.titleOptions)):
                g.titleOptions[i].update(g)

            g.screen.blit(self.image, (0,0))
            pg.display.flip()

    def end_fadeout(self, g):
        for i in range(16):
            g.clock.tick(FPS)
            self.image.set_alpha(i*16)

            g.bg.update(g)
            g.screen.blit(g.gameMapImg, (-g.camera.posx, -g.camera.posy))
            for i in range(len(g.blueCharList)):
                g.blueCharList[i].update(g)
            for i in range(len(g.redCharList)):
                g.redCharList[i].update(g)

            g.endScreenDialogue.update(g)
            g.endText.update(g)
            g.endSubText.update(g)

            g.screen.blit(self.image, (0,0))
            pg.display.flip()

    def start_fadein(self, g):
        for i in range(16):
            g.clock.tick(FPS)
            self.image.set_alpha(255-i*16)

            g.bg.update(g)
            g.screen.blit(g.gameMapImg, (-g.camera.posx, -g.camera.posy))
            for i in range(len(g.blueCharList)):
                g.blueCharList[i].update(g)
            for i in range(len(g.redCharList)):
                g.redCharList[i].update(g)
            g.turnText.update(g)

            g.screen.blit(self.image, (0,0))
            pg.display.flip()

    def end_fadein(self, g):
        for i in range(16):
            g.clock.tick(FPS)
            self.image.set_alpha(255-i*16)

            g.screen.blit(g.startScreenMapImg, g.startScreenPos)
            g.screen.blit(g.startScreenImg, (0,0))
            g.titleText.update(g)
            for i in range(len(g.titleOptions)):
                g.titleOptions[i].update(g)

            g.screen.blit(self.image, (0,0))
            pg.display.flip()

class Background(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        if not os.path.exists('content/img/bg.png'):
            shutil.copy('basecontent/img/bg.png','content/img')
        self.image = pg.image.load("content/img/bg.png")

    def update(self, g):
        for y in range(int(DISPLAY_HEIGHT/HEIGHT)):
            for x in range(int(DISPLAY_WIDTH/WIDTH)):
                if x*WIDTH not in range(int(-g.camera.posx), int(g.gameMap.width-g.camera.posx)) or y*HEIGHT not in range(int(-g.camera.posy), int(g.gameMap.height-g.camera.posy)):
                    g.screen.blit(self.image, (x*WIDTH, y*HEIGHT))

    def mini_update(self, g):
        for x in range(2):
            g.screen.blit(self.image, (x*WIDTH, 0))

def set_hp_colour(charObject):
    charObject.healthColour = list(colorsys.hsv_to_rgb(1/3.*charObject.hpfraction, 1, 1))
    for i in range(3):
        charObject.healthColour[i] *= 255
    charObject.hp_bar.image.fill(tuple(charObject.healthColour))

class HPBar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

class HPBarBorder(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        if not os.path.exists('content/img/hp_bar_border.png'):
            shutil.copy('basecontent/img/hp_bar_border.png','content/img')
        self.image = pg.image.load("content/img/hp_bar_border.png")

class BlueChar(pg.sprite.Sprite):
    def __init__(self, name, gender, img, stats, hp, weapon, pos, charTextContent):
        self.name = name
        self.gender = gender
        self.img = img
        self.stats = stats
        self.hp = hp
        self.weapon = weapon
        self.pos = pos
        self.gridPos = (int(self.pos[0]/WIDTH), int(self.pos[1]/HEIGHT))
        self.charTextContent = charTextContent

        self.image = pg.image.load('content/img/blue_' + self.gender + '/' + self.img + '.png')

        self.hp_bar_border = HPBarBorder()
        self.hp_bar = HPBar()

        self.active = True

    def update(self, g):
        if self.active == True or g.turn % 2 == 0:
            self.image = pg.image.load('content/img/blue_' + self.gender + '/' + self.img + '.png')
        if self.active == False and g.turn % 2 != 0:
            self.image = pg.image.load('content/img/blue_' + self.gender + '/' + self.img + '-inactive.png')

        self.gridPos = (int(self.pos[0]/WIDTH), int(self.pos[1]/HEIGHT))
        g.screen.blit(self.image, (self.pos[0] - g.camera.posx, self.pos[1] - g.camera.posy))
        g.screen.blit(self.hp_bar_border.image, (self.pos[0] - g.camera.posx, self.pos[1] - g.camera.posy))

        self.hpfraction = self.hp / MAX_HP
        self.hplength = math.ceil(self.hpfraction * HEALTH_BAR_LENGTH)

        self.hp_bar.image = pg.Surface((self.hplength, 2))
        set_hp_colour(self)
        g.screen.blit(self.hp_bar.image, (self.pos[0] - g.camera.posx + 16, self.pos[1] - g.camera.posy + 46))

    def get_range_loop(self, posy, posx, adjacentSquares):
        for i in range(4):
            if self.distance < MAX_DISTANCE and self.moveRange[adjacentSquares[i][0]][adjacentSquares[i][1]] != 2:
                self.distance += 1
                posx, posy = adjacentSquares[i][1], adjacentSquares[i][0]
                self.moveRange[posy][posx] = 1

                self.get_range_loop(posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

            elif self.distance == MAX_DISTANCE:
                self.distance -= 1
                return

        self.distance -= 1

    def get_range(self, g):
        self.distance = 0
        self.moveRange =  copy.deepcopy(g.gameMap.matrix)
        self.moveRange[self.gridPos[1]][self.gridPos[0]] = 1

        for y in range(len(self.moveRange)):
            for x in range(len(self.moveRange[y])):
                for i in range(len(g.redCharList)):
                    if (x, y) == g.redCharList[i].gridPos:
                        self.moveRange[y][x] = 2

        self.get_range_loop(self.gridPos[1], self.gridPos[0], [[self.gridPos[1], self.gridPos[0]+1], [self.gridPos[1]-1, self.gridPos[0]], [self.gridPos[1], self.gridPos[0]-1], [self.gridPos[1]+1, self.gridPos[0]]])

        for y in range(len(self.moveRange)):
            for x in range(len(self.moveRange[y])):
                for i in range(len(g.blueCharList)):
                    if (x, y) == g.blueCharList[i].gridPos and g.blueCharList[i] != self:
                        self.moveRange[y][x] = 0

    def get_atk_range_loop(self, g, posy, posx, adjacentSquares):
        weaponRange = self.weapon.get('range')
        for i in range(4):
            if self.distance < weaponRange and self.attackRange[adjacentSquares[i][0]][adjacentSquares[i][1]] != 2:
                self.distance += 1
                posx, posy = adjacentSquares[i][1], adjacentSquares[i][0]
                self.attackRange[posy][posx] = 1

                self.get_atk_range_loop(g, posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

            elif self.distance == weaponRange:
                self.distance -= 1
                return

        self.distance -= 1

    def get_atk_range(self, g):
        self.distance = 0
        self.attackRange = copy.deepcopy(g.gameMap.matrix)

        self.get_atk_range_loop(g, self.gridPos[1], self.gridPos[0], [[self.gridPos[1], self.gridPos[0]+1], [self.gridPos[1]-1, self.gridPos[0]], [self.gridPos[1], self.gridPos[0]-1], [self.gridPos[1]+1, self.gridPos[0]]])

class RedChar(pg.sprite.Sprite):
    def __init__(self, name, gender, img, stats, hp, weapon, pos, charTextContent):
        self.name = name
        self.gender = gender
        self.img = img
        self.stats = stats
        self.hp = hp
        self.weapon = weapon
        self.pos = pos
        self.gridPos = (int(self.pos[0]/WIDTH), int(self.pos[1]/HEIGHT))
        self.charTextContent = charTextContent

        self.image = pg.image.load('content/img/red_' + self.gender + '/' + self.img + '.png')

        self.hp_bar_border = HPBarBorder()
        self.hp_bar = HPBar()

        self.active = False

    def update(self, g):
        if self.active == True or g.turn % 2 != 0:
            self.image = pg.image.load('content/img/red_' + self.gender + '/' + self.img + '.png')
        if self.active == False and g.turn % 2 == 0:
            self.image = pg.image.load('content/img/red_' + self.gender + '/' + self.img + '-inactive.png')

        self.gridPos = (int(self.pos[0]/WIDTH), int(self.pos[1]/HEIGHT))
        g.screen.blit(self.image, (self.pos[0] - g.camera.posx, self.pos[1] - g.camera.posy))
        g.screen.blit(self.hp_bar_border.image, (self.pos[0] - g.camera.posx, self.pos[1] - g.camera.posy))

        self.hpfraction = self.hp / MAX_HP
        self.hplength = math.ceil(self.hpfraction * HEALTH_BAR_LENGTH)

        self.hp_bar.image = pg.Surface((self.hplength, 2))
        set_hp_colour(self)
        g.screen.blit(self.hp_bar.image, (self.pos[0] - g.camera.posx + 16, self.pos[1] - g.camera.posy + 46))

    def get_range_loop(self, posy, posx, adjacentSquares):
        for i in range(4):
            if self.distance < MAX_DISTANCE and self.moveRange[adjacentSquares[i][0]][adjacentSquares[i][1]] != 2:
                self.distance += 1
                posx, posy = adjacentSquares[i][1], adjacentSquares[i][0]
                self.moveRange[posy][posx] = 1

                self.get_range_loop(posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

            elif self.distance == MAX_DISTANCE:
                self.distance -= 1
                return

        self.distance -= 1

    def get_range(self, g):
        self.distance = 0
        self.moveRange =  copy.deepcopy(g.gameMap.matrix)
        self.moveRange[self.gridPos[1]][self.gridPos[0]] = 1

        for y in range(len(self.moveRange)):
            for x in range(len(self.moveRange[y])):
                for i in range(len(g.blueCharList)):
                    if (x, y) == g.blueCharList[i].gridPos:
                        self.moveRange[y][x] = 2

        self.get_range_loop(self.gridPos[1], self.gridPos[0], [[self.gridPos[1], self.gridPos[0]+1], [self.gridPos[1]-1, self.gridPos[0]], [self.gridPos[1], self.gridPos[0]-1], [self.gridPos[1]+1, self.gridPos[0]]])

        for y in range(len(self.moveRange)):
            for x in range(len(self.moveRange[y])):
                for i in range(len(g.redCharList)):
                    if (x, y) == g.redCharList[i].gridPos and g.redCharList[i] != self:
                        self.moveRange[y][x] = 0

    def get_atk_range_loop(self, g, posy, posx, adjacentSquares):
            weaponRange = self.weapon.get('range')
            for i in range(4):
                if self.distance < weaponRange and self.attackRange[adjacentSquares[i][0]][adjacentSquares[i][1]] != 2:
                    self.distance += 1
                    posx, posy = adjacentSquares[i][1], adjacentSquares[i][0]
                    self.attackRange[posy][posx] = 1

                    self.get_atk_range_loop(g, posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

                elif self.distance == weaponRange:
                    self.distance -= 1
                    return

            self.distance -= 1

    def get_atk_range(self, g):
            self.distance = 0
            self.attackRange =  copy.deepcopy(g.gameMap.matrix)

            self.get_atk_range_loop(g, self.gridPos[1], self.gridPos[0], [[self.gridPos[1], self.gridPos[0]+1], [self.gridPos[1]-1, self.gridPos[0]], [self.gridPos[1], self.gridPos[0]-1], [self.gridPos[1]+1, self.gridPos[0]]])

class PreMoveTile(pg.sprite.Sprite):
    def __init__(self, gridPos, charColour, activeStatus):
        self.gridPos = gridPos
        self.charColour = charColour
        self.activeStatus = activeStatus

        pg.sprite.Sprite.__init__(self)
        if not os.path.exists('content/img/preMoveTileInactive.png'):
            shutil.copy('basecontent/img/preMoveTileInactive.png','content/img')
        self.image = pg.image.load("content/img/preMoveTileInactive.png")

    def update(self, g):
        if self.charColour == 'red':
            if self.activeStatus == True or g.turn//2 != g.turn/2:
                if not os.path.exists('content/img/preMoveTileRed.png'):
                    shutil.copy('basecontent/img/preMoveTileRed.png','content/img')
                self.image = pg.image.load("content/img/preMoveTileRed.png")
            else:
                if not os.path.exists('content/img/preMoveTileInactive.png'):
                    shutil.copy('basecontent/img/preMoveTileInactive.png','content/img')
                self.image = pg.image.load("content/img/preMoveTileInactive.png")

        else:
            if self.activeStatus == True or g.turn//2 == g.turn/2:
                if not os.path.exists('content/img/preMoveTileBlue.png'):
                    shutil.copy('basecontent/img/preMoveTileBlue.png','content/img')
                self.image = pg.image.load("content/img/preMoveTileBlue.png")
            else:
                if not os.path.exists('content/img/preMoveTileInactive.png'):
                    shutil.copy('basecontent/img/preMoveTileInactive.png','content/img')
                self.image = pg.image.load("content/img/preMoveTileInactive.png")

        g.screen.blit(self.image, (self.gridPos[0]*WIDTH - g.camera.posx, self.gridPos[1]*HEIGHT - g.camera.posy))

class MoveTile(pg.sprite.Sprite):
    def __init__(self, gridPos, charColour):
        self.gridPos = gridPos
        self.colour = charColour
        if self.colour == 'blue':
            if not os.path.exists('content/img/moveTileBlue.png'):
                shutil.copy('basecontent/img/moveTileBlue.png','content/img')
            self.image = pg.image.load("content/img/moveTileBlue.png")

        if self.colour == 'red':
            if not os.path.exists('content/img/moveTileRed.png'):
                shutil.copy('basecontent/img/moveTileRed.png','content/img')
            self.image = pg.image.load("content/img/moveTileRed.png")

    def update(self, g):
        g.screen.blit(self.image, (self.gridPos[0]*WIDTH - g.camera.posx, self.gridPos[1]*HEIGHT - g.camera.posy))

class AttackTile(pg.sprite.Sprite):
    def __init__(self, gridPos):
        self.gridPos = gridPos

        pg.sprite.Sprite.__init__(self)
        if not os.path.exists('content/img/attackTile.png'):
            shutil.copy('basecontent/img/attackTile.png','content/img')
        self.image = pg.image.load("content/img/attackTile.png")

    def update(self, g):
        g.screen.blit(self.image, (self.gridPos[0]*WIDTH - g.camera.posx, self.gridPos[1]*HEIGHT - g.camera.posy))

class Cursor(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        if not os.path.exists('content/img/cursor.png'):
            shutil.copy('basecontent/img/cursor.png','content/img')
        self.image = pg.image.load("content/img/cursor.png")

    def update(self, g):
        g.screen.blit(self.image, ((g.x//WIDTH)*WIDTH, (g.y//HEIGHT)*HEIGHT))

class Text(pg.sprite.Sprite):
    def __init__(self, content, pos, size, colour):
        self.content = content
        self.pos = pos
        self.size = size
        self.colour = colour

        self.font = pg.font.SysFont(FONT, self.size, True)

        pg.sprite.Sprite.__init__(self)
        self.image = self.font.render(self.content, True, self.colour)

    def update(self, g):
        self.image = self.font.render(self.content, True, WHITE)
        g.screen.blit(self.image, self.pos)

class CenterText(pg.sprite.Sprite):
    def __init__(self, content, pos, size, colour):
        self.content = content
        self.pos = pos
        self.size = size
        self.colour = colour

        self.font = pg.font.SysFont(FONT, self.size, True)

        pg.sprite.Sprite.__init__(self)
        self.image = self.font.render(self.content, True, self.colour)

    def update(self, g):
        self.image = self.font.render(self.content, True, WHITE)
        g.screen.blit(self.image, (self.pos[0]-self.image.get_width()/2, self.pos[1]-self.image.get_height()/2))

class TitleOption(pg.sprite.Sprite):
    def __init__(self, g, content, size, colour):
        self.content = content
        self.size = size
        self.colour = colour
        self.pos = (70, 170+50*len(g.titleOptions))

        self.font = pg.font.SysFont(FONT, self.size, True)

        pg.sprite.Sprite.__init__(self)
        self.image = self.font.render(self.content, True, self.colour)

    def update(self, g):
        g.screen.blit(self.image, self.pos)
        self.rect = self.image.get_rect(topleft=self.pos)

    def hover(self):
        self.colour = LIGHTGREY
        self.image = self.font.render(self.content, True, self.colour)

    def no_hover(self):
        self.colour = WHITE
        self.image = self.font.render(self.content, True, self.colour)
