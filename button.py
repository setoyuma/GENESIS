import pygame as pg
from settings import FONT

class Button():

    def __init__(self, x, y, width, height, buttonText="button", onClickFunction=None, onePress=False):

        self.displaySurf = pg.display.get_surface()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.font = FONT

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pg.image.load('./assets/ui/buttons/button_plate1.png').convert_alpha()
        self.buttonSurface = pg.transform.scale(self.buttonSurface,(self.width,self.height))
        # self.buttonSurface = pg.Surface((self.width, self.height))
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)
        self.buttonRect.centerx = x
        self.buttonSurf = self.font.render(buttonText, True, "white")

    def Process(self):
        mousePos = pg.mouse.get_pos()
        # self.buttonSurface.fill(self.fillColors['normal'])

        if self.buttonRect.collidepoint(mousePos):
            # self.buttonSurface.fill(self.fillColors['hover'])

            if pg.mouse.get_pressed(num_buttons=3)[0]:
                # self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onClickFunction != None:
                    if self.onePress:
                        self.onClickFunction()
                        self.alreadyPressed = True

                    elif not self.alreadyPressed:
                        self.onClickFunction()
                        self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, (
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ))

        self.displaySurf.blit(self.buttonSurface, self.buttonRect)
