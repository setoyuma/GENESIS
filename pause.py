import pygame as pg
from support import check_for_quit, draw_text
from button import Button

class Pause:
    def __init__(self, game):
        self.game = game
        self.blurred_screen = pg.transform.gaussian_blur(game.screen, 8)
        self.buttons = [
		Button(self.game, "QUIT", (self.game.settings["screen_width"] - 100, 50,), pg.quit,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
		Button(self.game, "HOME", (100, 50,), pg.quit,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30)
		]
        
    def update(self):
        while self.game.paused:
            for event in pg.event.get():
                check_for_quit(event)
                for button in self.buttons:
                    button.update(event)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game.paused = False

                    if event.key == pg.K_r:
                        self.__init__()
                        self.MainMenu()

            self.game.screen.blit(self.blurred_screen, (0,0))
            pause = "PAUSED"
            draw_text(self.game.screen, f"PAUSE STATUS: {pause}", (self.game.settings["screen_width"]/2, 200))
            for button in self.buttons:
                button.draw()
            self.game.send_frame()