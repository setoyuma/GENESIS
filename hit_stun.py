import pygame as pg
from support import draw_text

class HitStunFrames:
    def __init__(self, game, stun_frames=3):
        self.game = game
        self.frame = 0
        self.stun_frames = stun_frames
        self.clock = pg.time.Clock()
        self.match_time = self.game.match_time

    def update(self):
        self.game.screen.fill('grey')
        self.game.drawBG()
        self.game.animate()
        self.dt = self.clock.tick(self.game.settings["FPS"])/2000

        COUNT_DOWN = pg.USEREVENT + 1   # sometimes 1/4 of a second slower than game clock

        for event in pg.event.get():
            if event.type == COUNT_DOWN:
                dt = self.dt
                self.match_time -= dt
                self.match_time_text = str(int(self.match_time)).rjust(3) if int(self.match_time) > 0 else 'GAME'
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_r:
                    self.game.__init__()
                    self.game.MainMenu()

        '''DRAW PLAYER'''
        self.game.player_2.draw()
        self.game.player_1.draw()

        if self.game.player_1.animated_text is not None:
            if self.game.player_1.animated_text.update():
                self.game.player_1.animated_text = None
        if self.game.player_2.animated_text is not None:
            if self.game.player_2.animated_text.update():
                self.game.player_2.animated_text = None
        
        #show player stats
        self.game.drawHealthBar(self.game.player_1)
        self.game.drawHealthBar(self.game.player_2)
        self.game.draw_HUD(self.game.screen)
        self.game.draw_portrait(self.game.player_1)
        self.game.draw_portrait(self.game.player_2)

        # match clock
        draw_text(self.game.screen, self.match_time_text[:-1], (self.game.settings["screen_width"]/2 - 70, 80), 100, (255, 0, 0))
        draw_text(self.game.screen, self.match_time_text[-1:], (self.game.settings["screen_width"]/2 + 50, 80), 100, (255, 0, 0))

        # show fps
        fpsCounter = str(int(self.game.clock.get_fps()))
        draw_text(self.game.screen, f"FPS: {fpsCounter}", (self.game.settings["screen_width"]/2, 200))

        pg.display.update()
        self.game.clock.tick(self.game.settings["FPS"])
        self.frame += 1
        pg.display.flip()
