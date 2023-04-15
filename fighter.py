import pygame as pg

from text_animation import TextAnimation
from particle import ParticlePrinciple
from projectile import Projectile
from animation import Animator
from constants import *
from support import *


class Event:
    def __init__(self, key=None):
        self.key = key


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
        self.super_meter = 0
        self.blast_meter = 0
        self.speed = 10

        # animations
        self.import_character_assets()
        self.status = 'idle'
        self.animation = self.animations[self.status]
        self.image = self.animation.animation[0]
        self.rect = pg.Rect(x, y, 150, 320)
        self.hit_box = pg.Rect(self.rect.x, self.rect.y - 100, 120, 280)
        self.AI = num - 1
        if self.AI:
            img = pg.transform.flip(self.image, True, False)
        self.particle = ParticlePrinciple()
        self.frame_index = 0  # for guest client

        # attacks
        self.time_since_last_input = 0
        self.move_combo = []
        self.blast_cooldown = 0
        self.attack_cooldown = 0
        self.time_without_combo = 0
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
        self.facing_right = not self.AI
        self.jumping = False
        self.hit = False

        # world
        self.dX = 0
        self.dY = 0
        self.gravity = 5000  # pps
        self.jump_force = -1800  # pps
        self.jump_cooldown = 0
        self.move_speed = 500  # pps

    def import_character_assets(self):
        self.animations = {}
        self.animation_keys = {'idle':[],'run':[],'jump':[],'crouch':[],'hit':[],'LP':[],'MP':[],'HP':[],'LK':[],'MK':[],'HK':[],'2LP':[],'2MP':[],'2HP':[],'2LK':[],'2MK':[],'2HK':[],'JLP':[],'JMP':[],'JHP':[],'JLK':[]} 
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
        input combo, and checks for valid combos.
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
            elif self.jumping:
                if str(event.key) in self.game.settings["attacks"]:
                    attack_key = "J" + self.game.settings["attacks"][str(event.key)]

            if attack_key is not None:
                self.status = attack_key
                self.attack_status = attack_key

        self.time_since_last_input = 0
        self.move_combo.append(event.key)

    ''' Updates things that are not frame-dependant.
        Animation is controlled by the player's status,
        which is updated after all key presses are handled.
    '''
    def update(self, dt, target):
        status = self.process_movement(dt)  # checks for movement input and adds to deltas
        self.update_cooldowns(dt)  # lowers jump and attack cooldowns
        self.update_combo_reset(dt)  # clear the combo list if time since last input is 0.45 seconds or there are 9 inputs
        self.update_position(dt, target)  # applies deltas and checks floor and walls
        self.update_animation(status, target)  # sets the animation according to a variety of conditions
        if self.projectile is not None:
            self.projectile.update(dt, target)  # mainly moves the projectile and checks for collisions

    def process_movement(self, dt):
        walking = False
        if (not self.attacking or not self.on_ground) and not self.game.hit_stun:
            # jump
            if self.pressed_keys[Actions.UP] and not self.jump_cooldown:
                self.dir = "UP"
                self.jump_cooldown = 0.7
                self.dY += self.jump_force
                self.jumping = True
                self.on_ground = False
                self.move_combo = []

            # crouch
            elif self.pressed_keys[Actions.DOWN] and self.on_ground:
                self.dir = "DOWN"
                self.crouching = True
                self.hit_box = pg.Rect(self.rect.x, self.rect.y -200, 120, 120)
                self.dX = 0
            else:
                self.crouching = False
                self.hit_box = pg.Rect(self.rect.x, self.rect.y - 100, 120, 280)
                self.animations["crouch"].reset()

            # strafe
            if not self.crouching:
                if self.pressed_keys[Actions.BACK]:
                    self.dir = "BACK"
                    self.rect.x -= self.move_speed * dt
                    if self.on_ground:
                        walking = True

                elif self.pressed_keys[Actions.FORWARD]:
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
        return status

    def update_cooldowns(self, dt):
        for attr_name in ['attack_cooldown', 'jump_cooldown']:
            cooldown = getattr(self, attr_name) - dt
            setattr(self, attr_name, max(cooldown, 0))

    def update_combo_reset(self, dt):
        self.time_since_last_input += dt
        if self.time_since_last_input > 0.083 or len(self.move_combo) > 9:
            self.time_since_last_input = 0
            self.check_combos()
            self.move_combo = []

    def update_position(self, dt, target):
        # update dY based on gravity
        self.dY += self.gravity * dt

        # update character's position based on deltas
        self.rect.x += self.dX * dt
        self.rect.y += self.dY * dt
        self.hit_box.center = self.rect.center

        # keep players facing each other
        if target.rect.centerx > self.rect.centerx:
            self.facing_right = True
        else:
            self.facing_right = False
        
        # make players push eachother/stop eachother on collision
        if self.rect.colliderect(target.rect) and self.facing_right and self.on_ground:
            # self.rect.right = target.rect.left
            target.rect.x += 3
        elif self.rect.colliderect(target.rect) and not self.facing_right and self.on_ground:
            # self.rect.left = target.rect.right
            target.rect.x -= 3

        # check walls
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.game.settings["screen_width"]:
            self.rect.right = self.game.settings["screen_width"]

        # check if the character is on the ground
        if self.rect.bottom >= 780:  # floor height
            self.rect.bottom = 780
            self.on_ground = True
            self.jumping = False
            self.animations["jump"].reset()
            self.dY = 0
        else:
            self.on_ground = False

    def update_animation(self, status, target):
        # cancel an attack if you are hit
        if self.attacking and self.hit:
            self.attacking = False

        # update animation status and image
        if not self.attacking:
            if self.status in ACTIONS:
                self.attacking = True
                self.attack_cooldown = 0.05  # seconds
            else:
                self.status = status
        elif self.status in ACTIONS and self.char_data["hitboxes"][self.status][0] == self.animation.frame_index:
            if not self.attacked:
                self.attack(target)

        if self.hit:
           self.status = "hit"

        self.animation = self.animations[self.status]
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
        if self.game.hit_stun:
            self.image = self.hit_frame
        else:
            self.image = self.animation.update(self.game.dt)

        if not self.facing_right:
            self.image = pg.transform.flip(self.image, True, False)

        self.game.screen.blit(self.image, (self.rect.x - 90, self.rect.y - 15))

        if self.projectile is not None:
            self.projectile.draw(self.game.screen)
            #pygame.draw.rect(self.game.screen, (0,255,0), self.projectile.rect)
        
        self.particle.emit()

    def attack(self, target, damage=None):
        # Get hitbox attributes for the active frame
        hitbox_attrs = self.char_data["hitboxes"]
        status = self.attack_status
        if damage is not None:
            status = "0"  # fireball doesnt need offset
        offset_x, offset_y, w, h = hitbox_attrs[status][1]

        # Calculate hitbox position using hitbox attributes and player rect
        flip_hit_box = self.rect.w
        if not self.facing_right:
            flip_hit_box *= -1
            offset_x = (offset_x * -1) - w
        x = self.hit_box.centerx + offset_x + flip_hit_box
        y = self.hit_box.centery + offset_y

        # Create the hitbox from all the attributes together
        attack_rect = pg.Rect(x, y, w, h)
        self.attack_rect = attack_rect

        # Detect collision on the active frame
        if (attack_rect.colliderect(target.hit_box) and not self.throwing_proj) or damage is not None:
            if target.alive:
                if damage is not None:  # passed in from projectile
                    fireball = True
                    play_sound('./assets/sfx/hit_1.wav')
                else:
                    fireball = False
                    damage = self.char_data["damage"][status]
                    self.handle_non_fireball_attack(target, status, damage, flip_hit_box, attack_rect)

                self.super_meter += damage * 2
                target.current_hp -= damage
                target.hit = True

                # Hitsparks and damage text
                self.hitspark(attack_rect, flip_hit_box, fireball, target)
                self.animated_text = TextAnimation("", 60, 0, target.hit_box.topright, "white", 30, self.game.screen)
                self.animated_text.damage = damage

                # Launch moves
                if self.character == "Homusubi" and status == "2HP" and target.hit:
                    target.dY -= 1800

                # Limit the super meter to 250
                if self.super_meter >= 250:
                    self.super_meter = 250

                # player death
                for player in self.game.players:
                    if player.current_hp <= 0:
                        player.current_hp = 0
                        player.alive = False

        elif not self.whiffed:
            self.whiffed = True
            play_sound('./assets/sfx/whiff_1.wav')

    def handle_non_fireball_attack(self, target, status, damage, flip_hit_box, attack_rect):
        self.attacked = True
        play_sound('./assets/sfx/hit_1.wav' if "L" in status or "M" in status else './assets/sfx/hit_2.wav')

        # Hit stun
        self.game.hit_stun = True
        self.game.stun_time = 0
        self.game.max_stun_time = 0.08
        self.hit_frame = self.animation.animation[self.animation.frame_index]
        player = self.game.player_1 if self.AI else self.game.player_2
        player.hit_frame = player.animation.animation[player.animation.frame_index]

        # Knockback
        if self.attacking and self.on_ground:
            self.rect.x -= 20 if self.facing_right else 20

    def hitspark(self, attack_rect, flip_hit_box, fireball, target):
        if not fireball:
            target_x, target_y = attack_rect.center
        else:
            target_x, target_y = target.hit_box.center
        for x in range(15):
            self.particle.addParticles(target_x, target_y, color="white")

    def check_combos(self):
        move_combo = self.move_combo if self.facing_right else [pg.K_a if key == pg.K_d else pg.K_d if key == pg.K_a else key for key in self.move_combo]
        self.perform_dp(move_combo)
        self.fire_projectile(move_combo)

    def fire_projectile(self, move_combo):
        if self.projectile is None:
            fireball_data = [("EXFireball", 98), ("LFireball", 40), ("MFireball", 98), ("HFireball", 98)]
            for proj_type, size in fireball_data:
                if move_combo == list(self.inputs[proj_type]) and self.super_meter >= 50:
                    print(proj_type)
                    self.projectile = Projectile("FSTECH", proj_type, size, self.rect.center, self, self.facing_right, self.game)
                    self.super_meter -= 50
                    self.throwing_proj = True
                    self.move_combo = []

    def perform_dp(self, move_combo):
        dp_data = ["LDP", "MDP", "HDP", "EXDP"]
        for name in dp_data:
            if move_combo == list(self.inputs[name]):
                self.dY -= 20
                self.move_combo = []
                print(name)

    def to_dict(self):
        return {
            'frame_index': self.animation.frame_index,
            'current_hp': self.current_hp,
            'super_meter': self.super_meter,
            'blast_meter': self.blast_meter,
            'speed': self.speed,
            'status': self.status,
            'rect': (self.rect.x, self.rect.y, self.rect.width, self.rect.height),
            'hit_box': (self.hit_box.x, self.hit_box.y, self.hit_box.width, self.hit_box.height),
            'on_ground': self.on_ground,
            'alive': self.alive,
            'facing_right': self.facing_right,
            'dX': self.dX,
            'dY': self.dY,
            'gravity': self.gravity,
            'jump_force': self.jump_force,
            'move_speed': self.move_speed
        }

    def from_dict(self, data):
        self.frame_index = data['frame_index']
        self.current_hp = data['current_hp']
        self.super_meter = data['super_meter']
        self.blast_meter = data['blast_meter']
        self.speed = data['speed']
        self.status = data['status']
        self.rect = pg.Rect(data['rect'][0], data['rect'][1], data['rect'][2], data['rect'][3])
        self.hit_box = pg.Rect(data['hit_box'][0], data['hit_box'][1], data['hit_box'][2], data['hit_box'][3])
        self.on_ground = data['on_ground']
        self.alive = data['alive']
        self.facing_right = data['facing_right']
        self.dX = data['dX']
        self.dY = data['dY']
        self.gravity = data['gravity']
        self.jump_force = data['jump_force']
        self.move_speed = data['move_speed']