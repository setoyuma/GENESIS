import pygame as pg
from support import check_for_quit

class Pause:
    def __init__(self, game):
        self.game = game
        self.blurred_screen = pg.transform.gaussian_blur(game.screen, 8)
        self.update()

    def update(self):
        while self.game.paused:
            self.game.screen.fill('black')
            self.game.screen.blit(self.game.background.update(self.game.dt), (-self.game.camera.rect.x, -self.game.camera.rect.y))

            for event in pg.event.get():
                check_for_quit(event)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game.paused = False

                    if event.key == pg.K_r:
                        self.__init__()
                        self.MainMenu()

                    if event.key == pg.K_h:
                        pg.draw.rect(self.game.screen, "green", self.game.player_1.hit_box)

            # draw players
            for player in self.game.players:
                player.draw()

            #show player stats
            self.game.draw_HUD()
            self.game.show_fps()

            for player in self.game.players:
                if player.animated_text is not None:
                    if player.animated_text.update():
                        player.animated_text = None

            
            self.game.screen.blit(self.blurred_screen, (0,0))
            self.game.send_frame()