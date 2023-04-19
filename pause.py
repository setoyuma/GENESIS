import pygame as pg
from support import check_for_quit, draw_text

class Pause:
    def __init__(self, game):
        self.game = game
        self.blurred_screen = pg.transform.gaussian_blur(game.screen, 8)

    def update(self):
        while self.game.paused:
            for event in pg.event.get():
                check_for_quit(event)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game.paused = False

                    if event.key == pg.K_r:
                        self.__init__()
                        self.MainMenu()

            self.game.screen.blit(self.blurred_screen, (0,0))
            pause = "PAUSED"
            draw_text(self.game.screen, f"PAUSE STATUS: {pause}", (self.game.settings["screen_width"]/2, 200))

            self.game.send_frame()