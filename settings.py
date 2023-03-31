import pygame as pg

pg.font.init()
FONT = pg.font.Font("assets/ui/font/minotaur.ttf", 30)

'''FIGHTER SCALES'''
fighter_scales = {
    1: 1,
}

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
