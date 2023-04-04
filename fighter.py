import pygame as pg

from text_animation import TextAnimation
from particle import ParticlePrinciple
from projectile import Projectile
from animation import Animator
from constants import *
from support import *


class Fighter:
    def __init__(self, game, num, x, y, char, mode="Play"):
        self.game = game
        self.character = char
        self.mode = mode

        # stats
        self.char_data = FIGHTER_DATA[char]
        self.current_hp = FIGHTER_DATA[char]["max hp"]
        self.size = FIGHTER_DATA[char]["size"]
        self.scale = FIGHTER_DATA[char]["scale"]
        self.inputs = FIGHTER_DATA[char]["combos"]  # combo names
        self.input_values = self.inputs.values() # combo moves
        self.super_meter = 0
        self.blast_meter = 0
        self.speed = 10

        # animations
        self.import_character_assets()
        self.status = 'idle'
        self.image = self.animations[self.status].animation[0]
        self.rect = pg.Rect(x, y, 150, 320)
        self.hit_box = pg.Rect(self.rect.x, self.rect.y - 100, 120, 280)
        self.AI = num - 1
        if self.AI:
            img = pg.transform.flip(self.image, True, False)
            # if in AI mode, init a pressed_keys dict for the AI to keep track of
            self.pressed_keys = pygame.key.get_pressed()
        self.particle = ParticlePrinciple()

        # attacks
        self.move_combo = []
        self.blast_cooldown = 0
        self.attack_cooldown = 0
        self.time_without_combo = 0
        self.hit_stun = None
        self.projectile = None
        self.throwing_proj = False
        self.animated_text = None
        self.frames_without_combo = 0
        self.whiffed = False
        self.attack_rect = None  # for debug

        # flags
        self.alive = True
        self.on_ground = True
        self.attacked = False
        self.attacking = False
        self.crouching = False
        self.walking = False
        self.facing_right = True
        self.jumping = False
        self.hit = False

        # world
        self.dX = 0
        self.dY = 0
        self.gravity = 5000  # pps
        self.jump_force = -1500  # pps
        self.jump_cooldown = 0
        self.move_speed = 500  # pps

    def import_character_assets(self):
        self.animations = {}
        self.animation_keys = {'idle':[],'run':[],'jump':[],'crouch':[],'hit':[],'LP':[],'MP':[],'HP':[],'LK':[],'MK':[],'HK':[],'2LP':[],'2MP':[],'2HP':[],'2LK':[],'2MK':[],'2HK':[]} 
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

    ''' Processes a single event. Updates single-press 
        inputs like basic attacks, updates the player's 
        input combo, then checks for valid combos.
    '''
    def handle_event(self, event):
        if not self.attacking and self.attack_cooldown == 0:
            attack_key = None
            if self.crouching:
                if event.key in (Actions.LP, Actions.MP, Actions.HP, Actions.LK, Actions.MK, Actions.HK):
                    attack_key = '2' + self.game.settings["attacks"][str(event.key)]
            elif self.on_ground:
                if str(event.key) in self.game.settings["attacks"]:
                    attack_key = self.game.settings["attacks"][str(event.key)]

            if attack_key is not None:
                self.status = attack_key
            
        self.move_combo.append(event.key)
        self.check_combos()

    ''' Updates things not related to frame-dependant
        Animation is controlled by the player's status,
        which is updated after all key presses are handled.
    '''
    def update(self, dt, target):
        if self.super_meter >= 250:
            self.super_meter = 250

        if self.current_hp <= 0:
            self.current_hp = 0
            self.alive = False
        if target.current_hp <= 0:
            target.current_hp = 0
            target.alive = False

        if self.AI:
            pressed_keys = self.pressed_keys
        else:
            pressed_keys = pg.key.get_pressed()

        walking = False

        if not self.attacking:
            # basic movements
            if pressed_keys[Actions.UP] and not self.jump_cooldown:
                self.dir = "UP"
                self.jump_cooldown = 0.9
                self.dY += self.jump_force
                self.jumping = True
                self.on_ground = False
                self.move_combo = []

            elif pressed_keys[Actions.DOWN] and self.on_ground:
                self.dir = "DOWN"
                self.crouching = True
                self.dX = 0

            else:
                self.crouching = False
                self.animations["crouch"].reset()

            if not self.crouching:
                if pressed_keys[Actions.BACK]:
                    self.dir = "BACK"
                    self.rect.x -= self.move_speed * dt
                    if self.on_ground:
                        walking = True

                elif pressed_keys[Actions.FORWARD]:
                    self.dir = "FORWARD"
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
            self.update_projectile(dt, target)

        self.frames_without_combo += 1
        if self.frames_without_combo > 26 or len(self.move_combo) > 9:
            self.frames_without_combo = 0
            self.move_combo = []

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
        self.hit_box.center = self.rect.center

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

        # keep players facing each other
        if target.rect.centerx > self.rect.centerx:
            self.facing_right = True
        else:
            self.facing_right = False

        # update animation status and image
        if not self.attacking:
            if self.status in ACTIONS :
                self.attacking = True
                self.attack_cooldown = 50 / 1000  # ms
            else:
                self.status = status
        elif self.status in ACTIONS and self.char_data["hitboxes"][self.status][0] == self.animation.frame_index:
            if not self.attacked:
                self.attack(target)

        if self.hit == True:
           self.status = 'hit'

        self.animation = self.animations[self.status]

        self.image = self.animation.update(dt)

        if not self.facing_right:
            self.image = pg.transform.flip(self.image, True, False)

        if self.animation.done and not self.animation.loop:
            if self.status in ACTIONS:
                self.animation.reset()
                self.attacking = False
                self.attacked = False
                self.whiffed = False
                self.status = "idle"
            if self.hit:
                self.animation.reset()
                self.hit = False

    def draw(self):
        #pygame.draw.rect(self.game.screen, (0,0,255), self.rect)
        #pygame.draw.rect(self.game.screen, (0,255,0), self.hit_box)
        self.game.screen.blit(self.image, (self.rect.x - 90, self.rect.y - 15))
        self.particle.emit()
        if self.projectile is not None:
            self.projectile.draw(self.game.screen)
            #pygame.draw.rect(self.game.screen, (0,255,0), self.projectile.rect)

    def attack(self, target, damage=None):
        # get hitbox attributes for the active frame
        hitbox_attrs = self.char_data["hitboxes"]
        status = self.status
        if damage is not None:
            status = "0"  # fireball doesnt need offset
        offset_x, offset_y, w, h = hitbox_attrs[status][1]
        # calculate hitbox position using hitbox attributes and player rect
        flip_hit_box = self.rect.w
        if not self.facing_right:
            flip_hit_box *= -1
            offset_x = (offset_x * -1) - w
        x = self.hit_box.centerx + offset_x + flip_hit_box
        y = self.hit_box.centery + offset_y
        # create the hitbox from all the attributes together
        attack_rect = pg.Rect(x, y, w, h)
        self.attack_rect = attack_rect
        # detect collision on the active frame
        if (attack_rect.colliderect(target.hit_box) and not self.throwing_proj) or damage is not None:
            if damage is None:
                fireball = False
                damage = self.char_data["damage"][status]
                self.super_meter += damage * 2
                if target.alive:
                    target.hit = True
                    self.attacked = True
                    if "L" in status:
                        play_sound('./assets/sfx/hit_1.wav')
                    if "M" in status:
                        play_sound('./assets/sfx/hit_1.wav')
                    if "H" in status:
                        play_sound('./assets/sfx/hit_2.wav')
                    target.current_hp -= damage
                    # target.max_hp -= self.char_data["damage"][status]
            elif damage:
                fireball = True
                self.super_meter += damage * 2
                if target.alive:
                    target.hit = True
                    target.current_hp -= damage
                    play_sound('./assets/sfx/hit_1.wav')

            '''LAUNCH MOVES'''
            match self.character:
                case "Homusubi":
                    if status == "2HP" and target.hit:
                        target.dY -= 1800
            self.hitspark(attack_rect, flip_hit_box, fireball, target)
            self.animated_text = TextAnimation("", 60, 0, target. hit_box.topright, "white", 30, self.game.screen)
            self.animated_text.damage = damage
            # hit stun
            if not fireball:
                self.game.hit_stun = True
                self.game.stun_frames = 0
                self.game.max_stun_frames = 3
            # knockback
            if self.attacking:
                if self.facing_right:
                    self.rect.x -= 20
                else:
                    self.rect.x += 20

        elif not self.whiffed:
            self.whiffed = True
            play_sound('./assets/sfx/whiff_1.wav')

    def hitspark(self, attack_rect, flip_hit_box, fireball=False, target=None):
        # calculate hitspark position based on attack_rect
        if not fireball:
            offset_x = 40
            target_x = attack_rect.x
            if self.facing_right:
                offset_x *= -1
                target_x += flip_hit_box
            target_x += offset_x
            target_y = attack_rect.centery
            if self.crouching:
                target_y += 70
        else:
            target_x, target_y = target.hit_box.center
        for x in range(15):
            self.particle.addParticles(target_x, target_y, color="white")

    def update_projectile(self, dt, target):
        self.projectile.animation.update(dt)
        self.projectile.move()

        # check if 50 ms has passed since projectile spawning
        self.projectile.frames_passed += 1
        if self.projectile.frames_passed >= 10:
            self.throwing_proj = False

        # check projectile collision with opponent
        if self.projectile.rect.collidepoint(target.rect.centerx, target.rect.centery+10):

            if self.projectile.type == "LFB":
                damage = 5
            elif self.projectile.type == "MFB":
                damage = 7
            elif self.projectile.type == "HFB":
                damage = 14

            target.hit = True
            self.projectile = None
            self.throwing_proj = False
            self.attack(target, damage)

        elif self.projectile.off_screen:
            self.projectile = None
            self.throwing_proj = False

    def check_combos(self):
        move_combo = self.move_combo
        if not self.facing_right:
            move_combo = [pg.K_a if key == pg.K_d else pg.K_d if key == pg.K_a else key for key in move_combo]

        for i in range(len(self.input_values)):
            if self.projectile is None:
                
                '''FIREBALLS'''
                if move_combo == list(self.inputs["LFireball"]) and self.super_meter >= 50:
                    self.projectile = Projectile("FSTECH", "LFB", 40, self.rect.center, self, self.facing_right, self.game)
                    self.super_meter -= 50

                elif move_combo == list(self.inputs["MFireball"]) and self.super_meter >= 50:
                    self.projectile = Projectile("FSTECH", "MFB", 98, self.rect.center, self, self.facing_right, self.game)
                    self.super_meter -= 50

                elif move_combo == list(self.inputs["HFireball"]) and self.super_meter >= 50:
                    self.projectile = Projectile("FSTECH", "HFB", 98, self.rect.center, self, self.facing_right, self.game)
                    self.super_meter -= 50

                '''DP'S'''
                if "LDP" in list(self.inputs):
                    if move_combo == list(self.inputs["LDP"]):
                        self.dY -= 20
                        self.move_combo = []
                        print("LDP")
                    elif move_combo == list(self.inputs["MDP"]):
                        self.dY -= 20
                        self.move_combo = []
                        print("MDP")
                    elif move_combo == list(self.inputs["HDP"]):
                        self.dY -= 20
                        self.move_combo = []
                        print("HDP")
                    elif move_combo == list(self.inputs["EXDP"]):
                        self.dY -= 20
                        self.move_combo = []
                        print("EXDP")
                else:
                    print("character has no dp")

                # check if a fireball has been created just now
                if self.projectile is not None:
                    self.projectile.frames_passed = 0
                    self.throwing_proj = True
                    self.move_combo = []