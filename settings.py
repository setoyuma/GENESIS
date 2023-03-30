import pygame as pg
pg.init()
pg.display.set_icon(pg.image.load('./assets/icons/main/gameicon.ico'))
HITSPARK = pg.image.load('./assets/vfx/hit/Hit-Spark8.png')

FPS = 60
screen_width = 1600
screen_height = 800
floor_height = 30
FONT = pg.font.Font("assets/ui/font/minotaur.ttf", 30)

'''FIGHTER SCALES'''
fighter_scales = {
    1: 1,
}

HALF_SCREENW = screen_width//2
HALF_SCREENH = screen_height//2
QUARTER_SCREENW = screen_width//4
QUARTER_SCREENH = screen_width//4

'''BACKGROUNDS'''
carnival = "bay-side-carnival"
ogre = "ogre-gate"

'''MUSIC'''
songs = {
    'main': 'assets/music/main/main.wav',
    'egypt': 'assets/music/egypt/egypt.wav',
    'science': 'assets/music/science/science_R1.wav',
    'q': 'assets/music/q/q.wav',
    'credits': 'assets/music/credits/credits.wav',
}
game_volume = 0.6

'''MOVEMENT'''
UP = pg.K_w
DOWN = pg.K_s
BACK = pg.K_a
FORWARD = pg.K_d

'''ATTACKS'''
LP = pg.K_i
MP = pg.K_o
HP = pg.K_p
LK = pg.K_k
MK = pg.K_l
HK = pg.K_SEMICOLON

# L_MP = LP and MP
# M_HP = pg.K_
# L_MK = pg.K_
# M_HK = pg.K_

