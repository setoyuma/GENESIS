import pygame as pg

from text_animation import TextAnimation
from particle import ParticlePrinciple
from projectile import Projectile
from animation import Animator
from constants import *
from support import *

"""
Animation update order:
attacks
crouch attacks
crouch

status update order:
attacks
jump
crouch
walk
idle
"""


class Fighter():
    def __init__(self, game, num, x, y, char, mode="Play"):
        self.game = game
        self.character = char
        self.mode = mode

        # stats
        self.max_hp = FIGHTER_DATA[char]["max hp"]
        self.size = FIGHTER_DATA[char]["size"]
        self.scale = FIGHTER_DATA[char]["scale"]
        self.super_meter = 0
        self.blast_meter = 0
        self.speed = 10

        # animations
        self.import_character_assets()
        self.status = 'idle'
        self.image = self.animations[self.status].animation[0]
        self.rect = pg.Rect(x, y, 150, 320)
        self.AI = num - 1
        if self.AI:
            img = pg.transform.flip(self.image, True, False)
            # if in AI mode, init a pressed_keys dict for the AI to keep track of
            self.pressed_keys = pygame.key.get_pressed()
        self.particle = ParticlePrinciple()

        # attacks
        self.move_combo = []
        self.input_values = []
        self.blast_cooldown = 0
        self.attack_cooldown = 0
        self.time_without_combo = 0
        self.hit_stun = None
        self.projectile = None
        self.launch_target = None
        self.animated_text = None

        # flags
        self.alive = True
        self.on_ground = True
        self.attacking = False
        self.crouching = False
        self.walking = False
        self.jumping = False
        self.hit = False

        # world
        self.dX = 0
        self.dY = 0
        self.gravity = 1400  # pps
        self.jump_force = -700  # pps
        self.jump_cooldown = 0
        self.move_speed = 300  # pps


    def import_character_assets(self):
        self.animations = {}
        self.animation_keys = {'idle':[],'run':[],'jump':[],'crouch':[],'hit':[],'LP':[],'MP':[],'HP':[],'LK':[],'MK':[],'HK':[],'2LP':[],'2MP':[],'2HP':[],'2LK':[], '2MK':[]} 
        for key in self.animation_keys:
            full_path = f'./assets/characters/{self.character}/{key}/'
            original_images = import_folder(full_path)
            scaled_images = scale_images(original_images, (self.size, self.size))
            if key in ["idle", "run"]:
                loop = True
            else:
                loop = False
            animation = Animator(self.game, scaled_images, FRAME_DURATIONS[key], loop)
            self.animations[key] = animation


    ''' Processes a single event from any event source.
        Updates single-press inputs like basic attacks,
        updates the player's move combo, then checks for
        valid combos and clears it if necessary.
    '''
    def handle_event(self, event):
        if not self.attacking and self.attack_cooldown == 0:
            attack_key = None

            if self.crouching:
                if event.key in (Actions.LP, Actions.MP, Actions.HP, Actions.LK, Actions.MK):#, Actions.HK):
                    attack_key = '2' + self.game.settings["attacks"][str(event.key)]
            elif self.on_ground:
                if str(event.key) in self.game.settings["attacks"]:
                    attack_key = self.game.settings["attacks"][str(event.key)]

            if attack_key is not None:
                self.status = attack_key

        self.move_combo.append(event.key)
        self.check_combos()


    ''' Updates things not related to frame-dependant input eg
        moving, gravity, jumping, launching, animations, etc.
        Animation is controlled by the player's animation status,
        which is updated after all key presses are handled.
    '''
    def update(self, dt):
        if self.AI:
            pressed_keys = self.pressed_keys
        else:
            pressed_keys = pg.key.get_pressed()

        walking = False

        if not self.attacking:
            # basic movements
            if pressed_keys[Actions.UP] and not self.jump_cooldown:
                self.jump_cooldown = 1.2
                self.dY += self.jump_force
                self.jumping = True
                self.on_ground = False

            elif pressed_keys[Actions.DOWN] and self.on_ground:
                self.crouching = True
                self.dX = 0

            else:
                self.crouching = False
                self.animations["crouch"].reset()

            if not self.crouching:
                if pressed_keys[Actions.BACK]:
                    self.rect.x -= self.move_speed * dt
                    if self.on_ground:
                        walking = True

                elif pressed_keys[Actions.FORWARD]:
                    self.rect.x += self.move_speed * dt
                    if self.on_ground:
                        walking = True

        if self.jumping:
            status = "jump"
        elif self.crouching:
            status = "crouch"
        elif walking:
            status = "run"
        else:
            status = "idle"

        if self.projectile is not None:
            self.update_projectile()

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            if self.attack_cooldown < 0:
                self.attack_cooldown = 0

        # apply jump cooldown
        if self.jump_cooldown > 0:
            self.jump_cooldown -= dt
            if self.jump_cooldown < 0:
                self.jump_cooldown = 0

        # update dY based on gravity
        self.dY += self.gravity * dt

        # update character's position based on deltas
        self.rect.x += self.dX * dt
        self.rect.y += self.dY * dt

        # check x // walls
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.game.settings["screen_width"]:
            self.rect.right = self.game.settings["screen_width"]

        # check y // if the character is on the ground
        if self.rect.bottom >= 780:  # floor height
            self.rect.bottom = 780
            self.on_ground = True
            self.jumping = False
            self.animations["jump"].reset()
            self.dY = 0
        else:
            self.on_ground = False

        # update animation status and image
        if not self.attacking:
            if self.status in ACTIONS:
                self.attacking = True
                self.attack_cooldown = 50 / 1000  # ms
            else:
                self.status = status

        self.animation = self.animations[self.status]
        self.image = self.animation.update(dt)

        if self.animation.done and not self.animation.loop:
            if self.status in ACTIONS:
                self.animation.reset()
                self.attacking = False
                self.status = "idle"
            #elif self.status == "crouch" and self.animation.done:
            #    self.image = self.animation.animation[-1]

    def draw(self):
        pygame.draw.rect(self.game.screen, (0,255,0), self.rect)
        self.game.screen.blit(self.image, (self.rect.x - 90, self.rect.y - 15))


    def update_projectile(self):
        # check if 50 ms has passed since proj spawning
        self.proj.frames_passed += 1
        if self.proj.frames_passed >= 10:
            self.throwing_proj = False

        # check projectile collision with opponent
        if self.proj.rect.collidepoint(target.rect.centerx, target.rect.centery-10):

            if self.proj.type == "LFB":
                damage = 5
            elif self.proj.type == "MFB":
                damage = 7
            elif self.proj.type == "HFB":
                damage = 14

            target.hit = True
            self.proj = None
            self.fireball = False
            self.throwing_proj = False
            # self.attack(target, damage)

        elif self.proj.off_screen:
            self.proj = None
            self.fireball = False
            self.throwing_proj = False

    def check_combos(self):
        pass