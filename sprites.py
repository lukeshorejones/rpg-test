import colorsys, copy, math, pygame as pg, shutil
from globals import *

def hp_colour(unit):
    hp_colour = list(colorsys.hsv_to_rgb(1/3.*unit.hp_fraction, 1, 1))
    for i in range(3):
        hp_colour[i] *= 255
    return tuple(hp_colour)

class StartScreenOverlay(pg.sprite.Sprite):
    def __init__(self, scalar):
        super().__init__()
        self.image = pg.image.load("content/img/start_screen_overlay.png")
        self.image = pg.transform.scale(self.image, (self.image.get_width(), DISPLAY_HEIGHT))

    def update(self, g):
        pass
        g.screen.blit(self.image, (0, 0))

class DialogueBox(pg.sprite.Sprite):
    def __init__(self, dim, pos):
        super().__init__()
        self.pos = pos

        self.image = pg.Surface(dim)
        self.image.fill(BLACK)
        self.image.set_alpha(204)

    def update(self, g):
        g.screen.blit(self.image, self.pos)

class PreviewBox(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("content/img/preview_box.png")
        self.border = pg.Surface((DISPLAY_WIDTH, 128))
        self.border.fill(BLACK)

    def update(self, g):
        if DISPLAY_WIDTH > 960:
            g.screen.blit(self.border, (0, g.game_height))
            g.screen.blit(self.image, (0, g.game_height))
        else:
            g.screen.blit(self.image, (0, g.game_height))

class Fade(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.image.fill(BLACK)

    def start_fade_out(self, g):
        for i in range(16):
            g.clock.tick(FPS)
            self.image.set_alpha(i*16)

            g.screen.blit(g.start_screen_map_img, g.start_screen_pos)
            g.start_screen_overlay.update(g)
            g.title_text.update(g)
            for i in range(len(g.title_options)):
                g.title_options[i].update(g)

            g.screen.blit(self.image, (0,0))
            pg.display.flip()

    def end_fade_out(self, g):
        for i in range(16):
            g.clock.tick(FPS)
            self.image.set_alpha(i*16)

            g.bg.update(g)
            g.screen.blit(g.map_img, (-g.cam.posx, -g.cam.posy))
            for i in range(len(g.blues)):
                g.blues[i].update(g)
            for i in range(len(g.reds)):
                g.reds[i].update(g)
            g.preview_box.update(g)
            g.turn_dialogue.update(g)
            g.turn_text.update(g)

            g.end_screen_dialogue.update(g)
            g.end_text.update(g)
            g.end_sub_text.update(g)

            g.screen.blit(self.image, (0,0))
            pg.display.flip()

    def start_fade_in(self, g):
        for i in range(16):
            g.clock.tick(FPS)
            self.image.set_alpha(255-i*16)

            g.bg.update(g)
            g.screen.blit(g.map_img, (-g.cam.posx, -g.cam.posy))
            for i in range(len(g.blues)):
                g.blues[i].update(g)
            for i in range(len(g.reds)):
                g.reds[i].update(g)
            g.preview_box.update(g)
            g.turn_dialogue.update(g)
            g.turn_text.update(g)

            g.screen.blit(self.image, (0,0))
            pg.display.flip()

    def end_fade_in(self, g):
        for i in range(16):
            g.clock.tick(FPS)
            self.image.set_alpha(255-i*16)

            g.screen.blit(g.start_screen_map_img, g.start_screen_pos)
            g.start_screen_overlay.update(g)
            g.title_text.update(g)
            for i in range(len(g.title_options)):
                g.title_options[i].update(g)

            g.screen.blit(self.image, (0,0))
            pg.display.flip()

class Background(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self, g):
        for y in range(int(g.game_height/HEIGHT)):
            for x in range(int(DISPLAY_WIDTH/WIDTH)):
                if x*WIDTH not in range(int(-g.cam.posx), int(g.map.width-g.cam.posx)) or y*HEIGHT not in range(int(-g.cam.posy), int(g.map.height-g.cam.posy)):
                    g.screen.blit(self.image, (x*WIDTH, y*HEIGHT))

    def turn_change_update(self, g):
        for x in range(int(DISPLAY_WIDTH/WIDTH)):
            if x*WIDTH not in range(int(-g.cam.posx), int(g.map.width-g.cam.posx)):
                g.screen.blit(self.image, (x*WIDTH, 3*HEIGHT))
                g.screen.blit(self.image, (x*WIDTH, 4*HEIGHT))
                g.screen.blit(self.image, (x*WIDTH, 5*HEIGHT))

class HPBar(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

class HPBarBorder(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("content/img/hp_bar_border.png")

class PreviewHPBar(pg.sprite.Sprite):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def set_img(self, g):
        if g.preview_one != None and self.num == 1:
            preview_hp_fraction = g.preview_one.hp / MAX_HP
            preview_hp_length = math.ceil(preview_hp_fraction * 100)

            self.image = pg.Surface((12, preview_hp_length))
            self.image.fill(hp_colour(g.preview_one))

        elif g.preview_two != None and self.num == 2:
            preview_hp_fraction = g.preview_two.hp / MAX_HP
            preview_hp_length = math.ceil(preview_hp_fraction * 100)

            self.image = pg.Surface((12, preview_hp_length))
            self.image.fill(hp_colour(g.preview_two))

    def update(self, g):
        if g.preview_one != None and self.num == 1:
            preview_hp_fraction = g.preview_one.hp / MAX_HP
            preview_hp_length = math.ceil(preview_hp_fraction * 100)
            g.screen.blit(self.image, (126, g.game_height+114-preview_hp_length))

        elif g.preview_two != None and self.num == 2:
            preview_hp_fraction = g.preview_two.hp / MAX_HP
            preview_hp_length = math.ceil(preview_hp_fraction * 100)
            g.screen.blit(self.image, (604, g.game_height+114-preview_hp_length))

class Blue(pg.sprite.Sprite):
    def __init__(self, name, gender, img, stats, hp, weapon, pos):
        super().__init__()
        self.colour = 'blue'
        self.name = name
        self.gender = gender
        self.img = img
        self.stats = stats
        self.hp = hp
        self.weapon = weapon
        self.pos = pos
        self.grid_pos = (int(self.pos[0]/WIDTH), int(self.pos[1]/HEIGHT))

        self.image = pg.image.load('content/img/blue_' + self.gender + '/' + self.img + '.png')

        self.hp_bar_border = HPBarBorder()
        self.hp_bar = HPBar()

        self.hp_fraction = self.hp / MAX_HP
        self.hp_length = math.ceil(self.hp_fraction * HEALTH_BAR_LENGTH)

        self.hp_bar.image = pg.Surface((self.hp_length, 2))
        self.hp_bar.image.fill(hp_colour(self))

        self.active = True

    def set_img(self, g):
        if self.active == True or g.turn % 2 == 0:
            self.image = pg.image.load('content/img/blue_' + self.gender + '/' + self.img + '.png')
        if self.active == False and g.turn % 2 != 0:
            self.image = pg.image.load('content/img/blue_' + self.gender + '/' + self.img + '-inactive.png')

    def set_hp_img(self, g):
        self.hp_fraction = self.hp / MAX_HP
        self.hp_length = math.ceil(self.hp_fraction * HEALTH_BAR_LENGTH)

        self.hp_bar.image = pg.Surface((self.hp_length, 2))
        self.hp_bar.image.fill(hp_colour(self))

    def update(self, g):
        self.grid_pos = (int(self.pos[0]/WIDTH), int(self.pos[1]/HEIGHT))
        g.screen.blit(self.image, (self.pos[0] - g.cam.posx, self.pos[1] - g.cam.posy))
        g.screen.blit(self.hp_bar_border.image, (self.pos[0] - g.cam.posx, self.pos[1] - g.cam.posy))
        g.screen.blit(self.hp_bar.image, (self.pos[0] - g.cam.posx + 16, self.pos[1] - g.cam.posy + 46))

    def get_range_loop(self, posy, posx, adjacent_tiles):
        for i in range(4):
            if self.distance < MAX_DISTANCE and self.move_range[adjacent_tiles[i][0]][adjacent_tiles[i][1]] != 2:
                self.distance += 1
                posx, posy = adjacent_tiles[i][1], adjacent_tiles[i][0]
                self.move_range[posy][posx] = 1

                self.get_range_loop(posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

            elif self.distance == MAX_DISTANCE:
                self.distance -= 1
                return

        self.distance -= 1

    def get_range(self, g):
        self.distance = 0
        self.move_range = copy.deepcopy(g.map.matrix)
        self.move_range[self.grid_pos[1]][self.grid_pos[0]] = 1

        for y in range(len(self.move_range)):
            for x in range(len(self.move_range[y])):
                for i in range(len(g.reds)):
                    if (x, y) == g.reds[i].grid_pos:
                        self.move_range[y][x] = 2

        self.get_range_loop(self.grid_pos[1], self.grid_pos[0], [[self.grid_pos[1], self.grid_pos[0]+1], [self.grid_pos[1]-1, self.grid_pos[0]], [self.grid_pos[1], self.grid_pos[0]-1], [self.grid_pos[1]+1, self.grid_pos[0]]])

    def get_atk_range_loop(self, g, posy, posx, adjacent_tiles):
        weaponRange = self.weapon.get('range')
        for i in range(4):
            if self.distance < weaponRange and self.attack_range[adjacent_tiles[i][0]][adjacent_tiles[i][1]] != 2:
                self.distance += 1
                posx, posy = adjacent_tiles[i][1], adjacent_tiles[i][0]
                self.attack_range[posy][posx] = 1

                self.get_atk_range_loop(g, posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

            elif self.distance == weaponRange:
                self.distance -= 1
                return

        self.distance -= 1

    def get_atk_range(self, g):
        self.distance = 0
        self.attack_range = copy.deepcopy(g.map.matrix)

        self.get_atk_range_loop(g, self.grid_pos[1], self.grid_pos[0], [[self.grid_pos[1], self.grid_pos[0]+1], [self.grid_pos[1]-1, self.grid_pos[0]], [self.grid_pos[1], self.grid_pos[0]-1], [self.grid_pos[1]+1, self.grid_pos[0]]])

class Red(pg.sprite.Sprite):
    def __init__(self, name, gender, img, stats, hp, weapon, pos):
        super().__init__()
        self.colour = 'red'
        self.name = name
        self.gender = gender
        self.img = img
        self.stats = stats
        self.hp = hp
        self.weapon = weapon
        self.pos = pos
        self.grid_pos = (int(self.pos[0]/WIDTH), int(self.pos[1]/HEIGHT))

        self.image = pg.image.load('content/img/red_' + self.gender + '/' + self.img + '.png')

        self.hp_bar_border = HPBarBorder()
        self.hp_bar = HPBar()

        self.hp_fraction = self.hp / MAX_HP
        self.hp_length = math.ceil(self.hp_fraction * HEALTH_BAR_LENGTH)

        self.hp_bar.image = pg.Surface((self.hp_length, 2))
        self.hp_bar.image.fill(hp_colour(self))

        self.active = False

    def set_img(self, g):
        if self.active == True or g.turn % 2 != 0:
            self.image = pg.image.load('content/img/red_' + self.gender + '/' + self.img + '.png')
        if self.active == False and g.turn % 2 == 0:
            self.image = pg.image.load('content/img/red_' + self.gender + '/' + self.img + '-inactive.png')

    def set_hp_img(self, g):
        self.hp_fraction = self.hp / MAX_HP
        self.hp_length = math.ceil(self.hp_fraction * HEALTH_BAR_LENGTH)

        self.hp_bar.image = pg.Surface((self.hp_length, 2))
        self.hp_bar.image.fill(hp_colour(self))

    def update(self, g):
        self.grid_pos = (int(self.pos[0]/WIDTH), int(self.pos[1]/HEIGHT))
        g.screen.blit(self.image, (self.pos[0] - g.cam.posx, self.pos[1] - g.cam.posy))
        g.screen.blit(self.hp_bar_border.image, (self.pos[0] - g.cam.posx, self.pos[1] - g.cam.posy))
        g.screen.blit(self.hp_bar.image, (self.pos[0] - g.cam.posx + 16, self.pos[1] - g.cam.posy + 46))

    def get_range_loop(self, posy, posx, adjacent_tiles):
        for i in range(4):
            if self.distance < MAX_DISTANCE and self.move_range[adjacent_tiles[i][0]][adjacent_tiles[i][1]] != 2:
                self.distance += 1
                posx, posy = adjacent_tiles[i][1], adjacent_tiles[i][0]
                self.move_range[posy][posx] = 1

                self.get_range_loop(posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

            elif self.distance == MAX_DISTANCE:
                self.distance -= 1
                return

        self.distance -= 1

    def get_range(self, g):
        self.distance = 0
        self.move_range = copy.deepcopy(g.map.matrix)
        self.move_range[self.grid_pos[1]][self.grid_pos[0]] = 1

        for y in range(len(self.move_range)):
            for x in range(len(self.move_range[y])):
                for i in range(len(g.blues)):
                    if (x, y) == g.blues[i].grid_pos:
                        self.move_range[y][x] = 2

        self.get_range_loop(self.grid_pos[1], self.grid_pos[0], [[self.grid_pos[1], self.grid_pos[0]+1], [self.grid_pos[1]-1, self.grid_pos[0]], [self.grid_pos[1], self.grid_pos[0]-1], [self.grid_pos[1]+1, self.grid_pos[0]]])

    def get_atk_range_loop(self, g, posy, posx, adjacent_tiles):
            weaponRange = self.weapon.get('range')
            for i in range(4):
                if self.distance < weaponRange and self.attack_range[adjacent_tiles[i][0]][adjacent_tiles[i][1]] != 2:
                    self.distance += 1
                    posx, posy = adjacent_tiles[i][1], adjacent_tiles[i][0]
                    self.attack_range[posy][posx] = 1

                    self.get_atk_range_loop(g, posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

                elif self.distance == weaponRange:
                    self.distance -= 1
                    return

            self.distance -= 1

    def get_atk_range(self, g):
            self.distance = 0
            self.attack_range =  copy.deepcopy(g.map.matrix)

            self.get_atk_range_loop(g, self.grid_pos[1], self.grid_pos[0], [[self.grid_pos[1], self.grid_pos[0]+1], [self.grid_pos[1]-1, self.grid_pos[0]], [self.grid_pos[1], self.grid_pos[0]-1], [self.grid_pos[1]+1, self.grid_pos[0]]])

class PreMoveTile(pg.sprite.Sprite):
    def __init__(self, grid_pos, unit_colour, active_status):
        super().__init__()
        self.grid_pos = grid_pos
        self.unit_colour = unit_colour
        self.active_status = active_status
        self.image = pg.image.load("content/img/pre_move_tile_inactive.png")

    def set_img(self, g):
        if self.unit_colour == 'red':
            if self.active_status == True or g.turn//2 != g.turn/2:
                self.image = pg.image.load("content/img/pre_move_tile_red.png")
            else:
                self.image = pg.image.load("content/img/pre_move_tile_inactive.png")

        else:
            if self.active_status == True or g.turn//2 == g.turn/2:
                self.image = pg.image.load("content/img/pre_move_tile_blue.png")
            else:
                self.image = pg.image.load("content/img/pre_move_tile_inactive.png")

    def update(self, g):
        g.screen.blit(self.image, (self.grid_pos[0]*WIDTH - g.cam.posx, self.grid_pos[1]*HEIGHT - g.cam.posy))

class MoveTile(pg.sprite.Sprite):
    def __init__(self, grid_pos, unit_colour):
        super().__init__()
        self.grid_pos = grid_pos
        self.colour = unit_colour
        if self.colour == 'blue':
            self.image = pg.image.load("content/img/move_tile_blue.png")

        if self.colour == 'red':
            self.image = pg.image.load("content/img/move_tile_red.png")

    def update(self, g):
        g.screen.blit(self.image, (self.grid_pos[0]*WIDTH - g.cam.posx, self.grid_pos[1]*HEIGHT - g.cam.posy))

class AttackTile(pg.sprite.Sprite):
    def __init__(self, grid_pos):
        super().__init__()
        self.grid_pos = grid_pos
        self.image = pg.image.load("content/img/attack_tile.png")

    def update(self, g):
        g.screen.blit(self.image, (self.grid_pos[0]*WIDTH - g.cam.posx, self.grid_pos[1]*HEIGHT - g.cam.posy))

class HealTile(pg.sprite.Sprite):
    def __init__(self, grid_pos):
        super().__init__()
        self.grid_pos = grid_pos
        self.image = pg.image.load("content/img/heal_tile.png")

    def update(self, g):
        g.screen.blit(self.image, (self.grid_pos[0]*WIDTH - g.cam.posx, self.grid_pos[1]*HEIGHT - g.cam.posy))

class Cursor(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("content/img/cursor.png")

    def update(self, g):
        g.screen.blit(self.image, ((g.x//WIDTH)*WIDTH, (g.y//HEIGHT)*HEIGHT))

class Text(pg.sprite.Sprite):
    def __init__(self, content, pos, size, colour):
        super().__init__()
        self.pos = pos
        self.size = size
        self.colour = colour

        self.font = pg.font.SysFont(FONT, self.size, True)
        self.image = self.font.render(content, True, self.colour)

    def set_content(self, content):
        self.image = self.font.render(content, True, WHITE)
    
    def update(self, g):
        g.screen.blit(self.image, self.pos)

class MultiLineText(pg.sprite.Sprite):
    def __init__(self, content, pos, size, colour):
        super().__init__()
        self.pos = pos
        self.size = size
        self.colour = colour
        
        self.images = []
        self.font = pg.font.SysFont(FONT, self.size, True)
        for line in content:
            self.images.append(self.font.render(line, True, self.colour))

    def set_content(self, content):
        self.images = []
        for line in content:
            self.images.append(self.font.render(line, True, self.colour))

    def update(self, g):
        for i in range(len(self.images)):
            g.screen.blit(self.images[i], (self.pos[0], self.pos[1]+((self.size+2)*i)))

class CenterText(pg.sprite.Sprite):
    def __init__(self, content, pos, size, colour):
        super().__init__()
        self.pos = pos
        self.size = size
        self.colour = colour

        self.font = pg.font.SysFont(FONT, self.size, True)
        self.image = self.font.render(content, True, self.colour)

    def set_content(self, content):
        self.image = self.font.render(content, True, WHITE)

    def update(self, g):
        g.screen.blit(self.image, (self.pos[0]-self.image.get_width()/2, self.pos[1]-self.image.get_height()/2))

class MenuOption(pg.sprite.Sprite):
    def __init__(self, g, content, size, colour, pos, centre):
        super().__init__()
        self.content = content
        self.size = size
        self.colour = colour
        self.pos = pos
        self.centre = centre

        self.font = pg.font.SysFont(FONT, self.size, True)
        self.image = self.font.render(self.content, True, self.colour)

        if self.centre == True:
            self.pos = (self.pos[0] - self.image.get_width()/2, self.pos[1])

    def update(self, g):
        g.screen.blit(self.image, self.pos)
        self.rect = self.image.get_rect(topleft=self.pos)

    def hover(self):
        self.colour = LIGHTGREY
        self.image = self.font.render(self.content, True, self.colour)

    def no_hover(self):
        self.colour = WHITE
        self.image = self.font.render(self.content, True, self.colour)

class PreviewPortrait(pg.sprite.Sprite):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def update(self, g):
        if g.preview_one != None and self.num == 1:
            self.colour = g.preview_one.colour
            self.gender = g.preview_one.gender
            self.img = g.preview_one.img

            self.image = pg.image.load('content/img/' + self.colour + '_' + self.gender + '/' + str(self.img) + '.png')
            self.image = pg.transform.scale2x(self.image)
            g.screen.blit(self.image, (0, g.game_height))

        elif g.preview_two != None and self.num == 2:
            self.colour = g.preview_two.colour
            self.gender = g.preview_two.gender
            self.img = g.preview_two.img

            self.image = pg.image.load('content/img/' + self.colour + '_' + self.gender + '/' + str(self.img) + '.png')
            self.image = pg.transform.scale2x(self.image)
            g.screen.blit(self.image, (478, g.game_height))

class PreviewWeaponImg(pg.sprite.Sprite):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def update(self, g):
        if g.preview_one != None and self.num == 1:
            self.img = g.preview_one.weapon.get('img')
            self.image = pg.image.load('content/img/weapons/' + str(self.img) + '.png')
            g.screen.blit(self.image, (258, g.game_height+16))

        elif g.preview_two != None and self.num == 2:
            self.img = g.preview_two.weapon.get('img')
            self.image = pg.image.load('content/img/weapons/' + str(self.img) + '.png')
            g.screen.blit(self.image, (736, g.game_height+16))
