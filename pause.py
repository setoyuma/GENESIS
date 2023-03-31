import pygame as pg
from support import draw_text, check_for_quit

class Pause:
    def __init__(self, game):
        self.game = game

    def update(self):
        while self.game.paused:
            self.game.screen.fill('grey')
            self.game.drawBG()

            for player in self.game.players:
                first_player = player == self.game.player_1

                if first_player:
                    other_player = self.game.player_2
                else:
                    other_player = self.game.player_1

                # process p1 events
                if first_player:
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

                # draw player
                player.draw()

            #show player stats
            self.game.draw_HUD()
            for player in self.game.players:
                if player.animated_text is not None:
                    if player.animated_text.update():
                        player.animated_text = None
            
            # match clock
            draw_text(self.game.screen, self.game.match_time_text[:-1], (self.game.settings["screen_width"]/2 - 70, 80), 100, (255, 0, 0))
            draw_text(self.game.screen, self.game.match_time_text[-1:], (self.game.settings["screen_width"]/2 + 50, 80), 100, (255, 0, 0))

            blurred_screen = pg.transform.gaussian_blur(self.game.screen, 8)
            self.game.screen.blit(blurred_screen, (0,0))
            self.game.send_frame()