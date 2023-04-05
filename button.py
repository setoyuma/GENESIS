import pygame as pg
from support import *
import sys

class Button:
    def __init__(self, game, text, pos, function, base=(0,0,300,81), hovered=(0,0,300,81), base_color=(77,77,255,50), hover_color=(77, 77, 80), text_color=(255,255,255), text_size=35, hovered_pos=None, id=None):
        self.game = game
        self.text = text
        self.pos = pos
        self.id = id
        self.function = function

        if isinstance(base, str):
            self.base = get_image(base)
            self.rect = self.base.get_rect()
            self.surf = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
            self.base_func = self.draw_image
        else:
            self.base = pygame.Rect(base)
            self.rect = self.base.copy()
            self.surf = pygame.Surface((base[2], base[3]), pygame.SRCALPHA)
            self.base_func = self.draw_rect
        self.center = self.surf.get_rect().center

        if isinstance(hovered, str):
            self.hovered = get_image(hovered)
            self.hover_func = self.draw_image
        else:
            self.hovered = pygame.Rect(hovered)
            self.hover_func = self.draw_rect

        self.rect.center = self.pos
        self.text_color = text_color
        self.base_color = base_color
        self.hover_color = hover_color
        self.size = text_size
        if hovered_pos is None:
            self.hovered_pos = pos
        else:
            self.hovered_pos = hovered_pos
        self.is_hovered = False
    
    def update(self, event):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos[0], pos[1]):
            self.is_hovered = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #play_sound("Assets/sounds/click.mp3")
                

                if isinstance(self.function, type):
                    self.game.sceneManager.scene = self.function(self.game)
                    return
                    



                if self.function != None:
                        if self.function == pg.quit:
                            self.function()
                            sys.exit()
                        elif self.id is not None:
                            self.function(self.id)
                        else:
                            self.function()                
                
        else:
            self.is_hovered = False

    def draw(self):
        self.surf.fill((0,0,0,0))
        if self.is_hovered:
            self.hover_func(self.hovered, self.hover_color)
        else:
            self.base_func(self.base, self.base_color)
        if self.text:
            draw_text(self.surf, self.text, self.center, self.size, self.text_color)
        self.game.screen.blit(self.surf, self.rect.topleft)

    def draw_rect(self, rect, color):
        pygame.draw.rect(self.surf, color, rect)

    def draw_image(self, image, color):
        self.surf.blit(image, (0,0))