import pygame
import sys

class Scene:
    def __init__(self, game, initial_bg=None):
        self.game = game
        self.active = True
        self.obscured = False

    def update(self):
        pass

    def draw(self):
        pass

    def check_universal_events(self, pressed_keys, event):
        quit_attempt = False
        if event.type == pygame.QUIT:
            quit_attempt = True
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or \
                            pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True
        if quit_attempt:
            pygame.quit()
            sys.exit()