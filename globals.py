import os, yaml
# Don't change any of these!

BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHTGREY = (211,211,211)

WIDTH, HEIGHT = 64, 64
HEALTH_BAR_LENGTH = 32

MOVE_STEPS = 8
MOVE_TIME = 0.02

# Initialising settings and config

config = yaml.load(open('content/config.yml'))
settings = yaml.load(open('content/settings.yml'))

TITLE = config.get('title')
FONT = config.get('font')
WIN_TEXT = config.get('win text')
LOSE_TEXT = config.get('lose text')
TIE_TEXT = config.get('tie text')
FPS = config.get('fps')
START_SCREEN_SPEED = config.get('start screen speed')
STAT_NAMES = config.get('stat names')
ENEMY_STAT_SPREAD = config.get('enemy stat spread')
MAX_HP = config.get('max hp')
MAX_DISTANCE = config.get('max distance')

DISPLAY_WIDTH = settings.get('display width')
DISPLAY_HEIGHT = settings.get('display height')
FULLSCREEN = settings.get('fullscreen')
VOLUME = settings.get('volume')
BLUE_PARTY = settings.get('blue party')
RED_PARTY = settings.get('red party')
