import pygame as pg
from support import draw_text
from settings import *

class HitStunFrames:
    def __init__(self, game, stun_frames=5):
        self.game = game
        self.frame = 0
        self.stun_frames = stun_frames
        while self.frame <= self.stun_frames:
            self.update()
    
    def update(self):
        self.game.screen.fill('grey')
        self.game.drawBG()
        self.game.animate()

        for event in pg.event.get():
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

        # show fps
        fpsCounter = str(int(self.game.clock.get_fps()))
        draw_text(self.game.screen, f"FPS: {fpsCounter}", (HALF_SCREENW, 200))

        pg.display.update()
        self.game.clock.tick(FPS)
        self.frame += 1
        pg.display.flip()
        self.game.clock.tick(FPS)
