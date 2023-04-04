import pygame as pg
import sys
# from settings import FONT

class Button():

    def __init__(self, game, x, y, width, height, size, buttonText="button", onClickFunction=None, id=None):
        self.game = game
        self.displaySurf = pg.display.get_surface()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        FONT = pg.font.Font('assets/ui/font/minotaur.ttf', size)
        self.font = FONT

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        image = pg.image.load('./assets/ui/buttons/button_plate1.png').convert_alpha()
        self.buttonSurface = pg.transform.scale(image, (self.width, self.height))
        #self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)
        self.buttonRect = pg.Rect(x, y, self.width, self.height)
        self.buttonRect.centerx, self.buttonRect.y = x, y
        self.buttonSurf = self.font.render(buttonText, True, "white")

        self.id = id

    def Process(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

            mousePos = pg.mouse.get_pos()
            if self.buttonRect.collidepoint(mousePos):

                    if self.onClickFunction != None:
                        if self.onClickFunction == pg.quit:
                            self.onClickFunction()
                            sys.exit()
                        elif self.onClickFunction == self.game.join_session:
                            self.game.join_session(self.id)
                        elif self.onClickFunction == self.game.leave_session:
                            self.game.leave_session()
                        else:
                            self.onClickFunction()

    def draw(self):
        self.buttonSurface.blit(self.buttonSurf, (self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2, self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ))

        self.displaySurf.blit(self.buttonSurface, self.buttonRect)
