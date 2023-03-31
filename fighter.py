import pygame as pg

from text_animation import TextAnimation
from particle import ParticlePrinciple
from projectile import Projectile
from animation import Animator
from show_inputs import Arrow
from animations import *
from constants import *
from support import *
from inputs import *


class Fighter():
    def __init__(self, game, x, y, char, mode="Play"):
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
        self.animation = Animator(game, self.animations["idle"], ANIMATION_SPEEDS["idle"], loop=True)
        if self == self.game.player_2: img = pg.transform.flip(self.image, True, False)
        self.status = 'idle'
        self.rect = pg.Rect(x, y, 80, 180)
        self.particle = ParticlePrinciple()
        self.alive = True

        # attacks
        self.fireball = False
        self.hit_stun = None
        self.attack_status = 'LP'
        self.attack_type = 0
        self.attack_cooldown = 0
        self.frames_without_combo = 0
        self.input_index = 0
        self.move_combo = []
        self.input_values = []
        self.move_damage = char_damage[self.character]

        # flags
        self.hit = False
        self.launch_target = None
        self.crouching = False
        self.on_ground = True
        self.walking = False
        self.jumping = False
        self.proj = None
        self.throwing_proj = False
        self.animated_text = None
        self.attacked = False
        self.attacking = False
        self.dashing = False
        self.facing_right = True

        # world
        self.dashGravity = 0.5
        self.dashLength = 40
        self.vel_y = 0
        self.GRAVITY = 2
        self.dir = "forward"
        self.arrow_locx = self.game.settings["screen_width"]/2-50
        self.arrow_locy = 200
        self.arrow_size = 96
        if self.mode == "Train":
            self.arrow = Arrow(self.dir, self.arrow_locx,
                               self.arrow_locy, self.arrow_size)

    def import_character_assets(self):
        match self.character:
            case "Homusubi":
                self.animations = Homusubi_Anims
            case "Raijin":
                self.animations = Raijin_Anims

        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'crouch':[],'hit':[],'LP':[],'MP':[],'HP':[],'LK':[],'MK':[],'HK':[],'2LP':[],'2MP':[],'2HP':[],'2LK':[]} 
        for animation in self.animations:
            full_path = f'./assets/characters/{self.character}/{animation}/'
            original_images = import_folder(full_path)
            scaled_images = scale_images(original_images, (self.size, self.size))
            self.animations[animation] = scaled_images

    ''' Updates things not related to input '''
    def update(self, target):
        self.walking = False
        self.dX = 0
        self.dY = 0
        if self == self.game.player_1:
            key = pg.key.get_pressed()
        else:
            key = [False]*300

        if not self.attacking and not self.throwing_proj:
            #movement
            if key[pg.K_a]:
                self.dir = "back"
                self.walking = True
                self.dX = - self.speed

                if self.mode == "Train":
                    self.arrow = Arrow(self.dir, self.arrow_locx, self.arrow_locy, self.arrow_size)

            if key[pg.K_d]:
                self.dir = "forward"
                self.walking = True
                self.dX = self.speed

                if self.mode == "Train":
                    self.arrow = Arrow(self.dir, self.arrow_locx, self.arrow_locy, self.arrow_size)

            #jump
            if key[pg.K_w] and self.on_ground and not self.jumping:
                self.dir = "up"
                self.vel_y = -30
                self.jumping = True
                self.on_ground = False

                if self.mode == "Train":
                    self.arrow = Arrow(self.dir, self.arrow_locx, self.arrow_locy, self.arrow_size)


            if key[pg.K_s] and self.on_ground:
                self.dir = "down"
                self.crouching = True
                self.dX = 0
                
                if self.mode == "Train":
                    self.arrow = Arrow(self.dir, self.arrow_locx, self.arrow_locy, self.arrow_size)

                # cancel movement
                if key[pg.K_w]:
                    self.dY = 0
                if key[pg.K_a]:
                    self.dX = 0
                if key[pg.K_d]:
                    self.dX = 0
            else:
                self.crouching = False

            '''DIAGONALS'''
            if key[pg.K_a] and key[pg.K_w]:
                self.dir = "up-back"

                if self.mode == "Train":
                    self.arrow = Arrow(self.dir, self.arrow_locx, self.arrow_locy, self.arrow_size)

            if key[pg.K_a] and key[pg.K_s]:
                self.dir = "down-back"

                if self.mode == "Train":
                    self.arrow = Arrow(self.dir, self.arrow_locx, self.arrow_locy, self.arrow_size)

            if key[pg.K_d] and key[pg.K_w]:
                self.dir = "up-forward"

                if self.mode == "Train":
                    self.arrow = Arrow(self.dir, self.arrow_locx, self.arrow_locy, self.arrow_size)


            if key[pg.K_d] and key[pg.K_s]:
                self.dir = "down-forward"

                if self.mode == "Train":
                    self.arrow = Arrow(self.dir, self.arrow_locx, self.arrow_locy, self.arrow_size)

        if self.mode == "Train":
            self.arrow.update()

        self.jump()

        if self.proj is not None:
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
                self.attack(target, damage)

            elif self.proj.off_screen:
                self.proj = None
                self.fireball = False
                self.throwing_proj = False

        #check screen loc
        if self.rect.left + self.dX < 0:
            self.dX = -self.rect.left
        if self.rect.right + self.dX > self.game.settings["screen_width"]:
            self.dX = self.game.settings["screen_width"] - self.rect.right

        #keep players facing
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
            self.facing_right = True
            self.facing_right = True
        else:
            self.flip = True
            self.facing_right = False
            self.facing_right = False

        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #check ground
        if self.rect.bottom + self.dY > self.game.settings["screen_height"] - self.game.settings["floor_height"]:
            self.on_ground = True
            self.vel_y = 0
            self.jumping = False
            self.dY = self.game.settings["screen_height"] - self.game.settings["floor_height"] - self.rect.bottom

        #update pos
        self.rect.x += self.dX
        self.rect.y += self.dY
        self.dashing = False

    ''' Processes a single event from any event source '''
    def handle_event(self, event):
        pass