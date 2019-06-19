import colorsys, copy, math, pygame as pg, shutil
from globals import *


def hp_colour(unit):
    hp_colour = list(colorsys.hsv_to_rgb(1/3.*unit.hp_fraction, 1, 1))
    for i in range(3):
        hp_colour[i] *= 255
    return tuple(hp_colour)


class MapPreviewImg(pg.sprite.Sprite):
    def __init__(self, dim, box):
        self.dim = dim
        self.pos = (box.pos[0] + (box.dim[0] - self.dim[0]) // 2, box.pos[1] + (box.dim[1] - self.dim[1]) // 2)

    def set_img(self, path):
        self.image = pg.image.load(path)

    def set_blank(self):
        self.image = pg.Surface(self.dim)
        self.image.fill(BLACK)

    def update(self, g):
        g.screen.blit(self.image, self.pos)


class Bar(pg.sprite.Sprite):
    def __init__(self, dim, colour, pos):
        super().__init__()
        self.dim = dim
        self.colour = colour
        self.pos = pos

        self.image = pg.Surface(self.dim)
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.rect = pg.Rect(self.rect.left - 5, self.rect.top - 5, self.rect.width + 10, self.rect.height + 10)

    def update_width(self, width):
        self.dim = (width, self.dim[1])
        self.image = pg.Surface(self.dim)
        self.image.fill(self.colour)

    def update(self, g):
        g.screen.blit(self.image, self.pos)


class Scrollbar(pg.sprite.Sprite):
    def __init__(self, dim, colour, base_pos):
        super().__init__()
        self.dim = dim
        self.colour = colour
        self.base_pos = base_pos
        self.remainder = 0

    def update_length(self, length):
        self.dim = (self.dim[0], length)
        self.image = pg.Surface(self.dim)
        self.image.fill(self.colour)

    def adjust_length(self, g):
        self.remainder = g.scrollbar_bg_length % self.dim[1]
        if self.remainder == 0:
            self.image = pg.Surface(self.dim)
            self.image.fill(self.colour)
        elif g.map_scroll_index > g.max_map_scroll_index - self.remainder:
            dim = (self.dim[0], self.dim[1] + 1)
            self.image = pg.Surface(dim)
            self.image.fill(self.colour)

    def set_pos(self, g):
        buffer = g.map_scroll_index - g.max_map_scroll_index + self.remainder - 1
        if buffer > 0:
            self.pos = (self.base_pos[0], self.base_pos[1] + g.map_scroll_index * self.dim[1] + buffer)
        else:
            self.pos = (self.base_pos[0], self.base_pos[1] + g.map_scroll_index * self.dim[1])

    def update(self, g):
        g.screen.blit(self.image, self.pos)


class Slider():
    def __init__(self, dim, pos, settings, volume_type, bar_colour, fill_colour, text_colour, g):
        self.volume_type = volume_type

        self.bar = Bar(dim, bar_colour, pos)
        self.fill_bar = Bar((settings.get(volume_type) * dim[0], dim[1]), fill_colour, pos)
        self.button = SliderButton(volume_type, (pos[0]-7, pos[1]-5), g)
        self.text = Text("100", (pos[0] + 217, pos[1] - 10), 20, text_colour)

    def set_selected_slider(self, g):
        g.selected_slider = self
        self.button.image = pg.image.load("content/img/slider_selected.png")

    def unset_selected_slider(self, g):
        g.selected_slider = None
        self.button.image = pg.image.load("content/img/slider.png")

    def update(self, g):
        volume = int(g.settings.get(self.volume_type)*100)
        if int(self.text.content) != volume:
            self.text.set_content(str(volume))
        self.bar.update(g)
        self.fill_bar.update(g)
        self.button.update(g)
        self.text.update(g)


class SliderButton(pg.sprite.Sprite):
    def __init__(self, volume_type, default_pos, g):
        super().__init__()
        self.volume_type = volume_type
        self.default_pos = default_pos

        self.image = pg.image.load("content/img/slider.png")
        self.pos = (self.default_pos[0] + g.settings.get(volume_type)*200, self.default_pos[1])

    def update_pos(self, pos):
        self.pos = pos

    def update(self, g):
        g.screen.blit(self.image, self.pos)


class StartScreenOverlay(pg.sprite.Sprite):
    def __init__(self, scalar):
        super().__init__()
        self.image = pg.image.load("content/img/start_screen_overlay.png")
        self.image = pg.transform.scale(self.image, (self.image.get_width(), DISPLAY_HEIGHT))

    def update(self, g):
        g.screen.blit(self.image, (0, 0))


class DialogueBox(pg.sprite.Sprite):
    def __init__(self, dim, pos):
        super().__init__()
        self.dim = dim
        self.pos = pos

        self.image = pg.Surface(self.dim)
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
    def __init__(self, elite):
        super().__init__()
        if elite:
            self.image = pg.image.load("content/img/hp_bar_border_elite.png")
        else:
            self.image = pg.image.load("content/img/hp_bar_border.png")


class PreviewHPBar(pg.sprite.Sprite):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def set_img(self, g):
        if g.preview_one is not None and self.num == 1:
            preview_hp_fraction = g.preview_one.hp / MAX_HP
            preview_hp_length = math.ceil(preview_hp_fraction * 100)

            self.image = pg.Surface((12, preview_hp_length))
            self.image.fill(hp_colour(g.preview_one))

        elif g.preview_two is not None and self.num == 2:
            preview_hp_fraction = g.preview_two.hp / MAX_HP
            preview_hp_length = math.ceil(preview_hp_fraction * 100)

            self.image = pg.Surface((12, preview_hp_length))
            self.image.fill(hp_colour(g.preview_two))

    def update(self, g):
        if g.preview_one is not None and self.num == 1:
            preview_hp_fraction = g.preview_one.hp / MAX_HP
            preview_hp_length = math.ceil(preview_hp_fraction * 100)
            g.screen.blit(self.image, (126, g.game_height+114-preview_hp_length))

        elif g.preview_two is not None and self.num == 2:
            preview_hp_fraction = g.preview_two.hp / MAX_HP
            preview_hp_length = math.ceil(preview_hp_fraction * 100)
            g.screen.blit(self.image, (604, g.game_height+114-preview_hp_length))


class Unit(pg.sprite.Sprite):
    def __init__(self, colour, elite, name, gender, img, stats, hp, weapon, trait, pos):
        super().__init__()
        self.colour = colour
        self.elite = elite
        self.name = name
        self.gender = gender
        self.img = img
        self.stats = stats
        self.hp = hp
        self.weapon = weapon
        self.trait = trait
        self.pos = pos
        self.grid_pos = (int(self.pos[0]/WIDTH), int(self.pos[1]/HEIGHT))

        self.image = pg.image.load('content/img/' + self.colour + '_' + self.gender + '/' + self.img + '.png')

        self.hp_bar_border = HPBarBorder(elite)
        self.hp_bar = HPBar()

        self.hp_fraction = self.hp / MAX_HP
        self.hp_length = math.ceil(self.hp_fraction * HEALTH_BAR_LENGTH)

        self.hp_bar.image = pg.Surface((self.hp_length, 2))
        self.hp_bar.image.fill(hp_colour(self))

        self.active = True

    def set_img(self, g):
        if (self.colour == 'blue' and (self.active or g.turn % 2 == 0)) or (self.colour == 'red' and (self.active or g.turn % 2 != 0)):
            self.image = pg.image.load('content/img/' + self.colour + '_' + self.gender + '/' + self.img + '.png')
        else:
            self.image = pg.image.load('content/img/' + self.colour + '_' + self.gender + '/' + self.img + '-inactive.png')

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

        if self.colour == 'blue':
            defenders = g.reds
        else:
            defenders = g.blues

        for y in range(len(self.move_range)):
            for x in range(len(self.move_range[y])):
                for i in range(len(defenders)):
                    if (x, y) == defenders[i].grid_pos:
                        self.move_range[y][x] = 2

        self.get_range_loop(self.grid_pos[1], self.grid_pos[0], [[self.grid_pos[1], self.grid_pos[0]+1], [self.grid_pos[1]-1, self.grid_pos[0]], [self.grid_pos[1], self.grid_pos[0]-1], [self.grid_pos[1]+1, self.grid_pos[0]]])

    def get_atk_range_loop(self, g, posy, posx, adjacent_tiles):
        weapon_range = self.weapon.get('range')
        for i in range(4):
            if self.distance < weapon_range and self.attack_range[adjacent_tiles[i][0]][adjacent_tiles[i][1]] != 2:
                self.distance += 1
                posx, posy = adjacent_tiles[i][1], adjacent_tiles[i][0]
                self.attack_range[posy][posx] = 1

                self.get_atk_range_loop(g, posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

            elif self.distance == weapon_range:
                self.distance -= 1
                return

        self.distance -= 1

    def get_atk_range(self, g):
        self.distance = 0
        self.attack_range = copy.deepcopy(g.map.matrix)

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
            if self.active_status or g.turn//2 != g.turn/2:
                self.image = pg.image.load("content/img/pre_move_tile_red.png")
            else:
                self.image = pg.image.load("content/img/pre_move_tile_inactive.png")

        else:
            if self.active_status or g.turn//2 == g.turn/2:
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
        self.content = content
        self.pos = pos
        self.size = size
        self.colour = colour

        self.font = pg.font.SysFont(FONT, self.size, True)
        self.image = self.font.render(self.content, True, self.colour)

    def set_content(self, content):
        self.content = content
        self.image = self.font.render(self.content, True, self.colour)

    def update(self, g):
        g.screen.blit(self.image, self.pos)
        # pg.draw.rect(g.screen, WHITE, self.image.get_rect(topleft=self.pos), 1)


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

    def auto_set_lines(self, raw, length):
        self.images = []
        words = raw.split()

        while words:
            line = ""
            i = 0
            while i < len(words) and self.font.size(line + words[i])[0] <= length:
                line = line + words[i] + " "
                i += 1
            words = words[len(line.split()):len(words)]
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
    def __init__(self, g, content, size, colour, base_pos, rect_buffer, centre):
        super().__init__()
        self.content = content
        self.size = size
        self.colour = colour
        self.base_pos = base_pos
        self.rect_buffer = rect_buffer
        self.centre = centre

        self.pos = base_pos

        self.font = pg.font.SysFont(FONT, self.size, True)
        self.image = self.font.render(self.content, True, self.colour)

        if self.centre:
            self.base_pos = (self.base_pos[0] - self.image.get_width()/2, self.base_pos[1])

        self.base_rect = self.image.get_rect(topleft=self.pos)
        self.base_rect = pg.Rect(self.base_rect.left - self.rect_buffer, self.base_rect.top - self.rect_buffer, self.base_rect.width + self.rect_buffer * 2, self.base_rect.height + self.rect_buffer * 2)
        self.rect = self.base_rect

    def update_base_pos_rect(self):
        self.base_pos = (self.base_pos[0], self.pos[1])
        self.base_rect = self.image.get_rect(topleft=self.pos)
        self.base_rect = pg.Rect(self.base_rect.left - self.rect_buffer, self.base_rect.top - self.rect_buffer, self.base_rect.width + self.rect_buffer * 2, self.base_rect.height + self.rect_buffer * 2)
        self.rect = self.base_rect

    def update(self, g):
        g.screen.blit(self.image, self.pos)
        # pg.draw.rect(g.screen, WHITE, self.rect, 1)

    def hover(self):
        if not self.centre:
            self.pos = (self.base_pos[0] + 20, self.base_pos[1])
            self.rect = pg.Rect(self.base_rect.left, self.base_rect.top, self.base_rect.width+20, self.base_rect.height)
        self.colour = LIGHTGREY
        self.image = self.font.render(self.content, True, self.colour)

    def no_hover(self):
        if not self.centre:
            self.pos = self.base_pos
            self.rect = self.base_rect
        self.colour = WHITE
        self.image = self.font.render(self.content, True, self.colour)


class PreviewPortrait(pg.sprite.Sprite):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def update(self, g):
        if g.preview_one is not None and self.num == 1:
            self.colour = g.preview_one.colour
            self.gender = g.preview_one.gender
            self.img = g.preview_one.img

            self.image = pg.image.load('content/img/' + self.colour + '_' + self.gender + '/' + str(self.img) + '.png')
            self.image = pg.transform.scale2x(self.image)
            g.screen.blit(self.image, (0, g.game_height))

        elif g.preview_two is not None and self.num == 2:
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
        if g.preview_one is not None and self.num == 1:
            self.img = g.preview_one.weapon.get('img')
            self.image = pg.image.load('content/img/weapons/' + str(self.img) + '.png')
            g.screen.blit(self.image, (258, g.game_height+16))

        elif g.preview_two is not None and self.num == 2:
            self.img = g.preview_two.weapon.get('img')
            self.image = pg.image.load('content/img/weapons/' + str(self.img) + '.png')
            g.screen.blit(self.image, (736, g.game_height+16))

class PreviewTraitImg(pg.sprite.Sprite):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def update(self, g):
        if self.num == 1 and g.preview_one is not None and g.preview_one.trait != {}:
            self.img = g.preview_one.trait.get('img')
            self.image = pg.image.load('content/img/traits/' + str(self.img) + '.png')
            g.screen.blit(self.image, (366, g.game_height+16))

        elif self.num == 2 and g.preview_two is not None and g.preview_two.trait != {}:
            self.img = g.preview_two.trait.get('img')
            self.image = pg.image.load('content/img/traits/' + str(self.img) + '.png')
            g.screen.blit(self.image, (844, g.game_height+16))
