import pygame as pg
from settings import *

from text_animation import TextAnimation
from hit_boxes import hit_boxes
from support import *
from inputs import *
from projectile import Projectile
from show_inputs import Arrow
from animations import *
from attack_damage import char_damage
from particle import ParticlePrinciple

attacks = ['LP', 'MP', 'HP', 'LK', 'MK', 'HK', '2LP', '2MP', '2HP']

class Fighter():
    def __init__(self, game, x, y, flip, surface, char, data, sprite_sheet, animation_steps, mode):
        self.game = game
        self.super_meter = 0
        self.character = char
        self.size = data[0]
        self.import_character_assets()
        self.frame_index = 0
        self.image = self.animations['idle'][self.frame_index]
        self.rect = pg.Rect(x, y, 80, 180)
        self.flip = flip
        self.mode = mode
        self.image_scale = data[1]
        self.offset = data[2]
        self.vel_y = 0
        self.walking = False
        self.jumping = False
        self.move_damage = char_damage[self.character]
        self.particle = ParticlePrinciple()
        self.proj = None
        self.throwing_proj = False
        self.animated_text = None

        '''FIREBALLS'''
        self.fireball = False
        if self.character == "Homusubi":
            pass

        self.hit = False
        self.crouching = False
        self.on_ground = True
        self.dir = "forward"
        self.arrow_locx = screen_width/2-50
        self.arrow_locy = 200
        self.arrow_size = 96
        if self.mode == "Train":
            self.arrow = Arrow(self.dir, self.arrow_locx,
                               self.arrow_locy, self.arrow_size)
        self.attacked = False
        self.attacking = False
        self.dashing = False
        self.attack_type = 0
        self.surface = surface
        self.hp = data[3]
        self.GRAVITY = 2
        self.dashGravity = 0.5
        self.dashLength = 40
        self.attack_cooldown = 0
        # attacks
        self.moveCombo = []
        self.framesWithoutCombo = 0
        self.inputIndex = 0
        self.inputs = {}
        self.inputValues = []
        self.inputKey = []

        self.status = 'idle'
        self.attack_status = 'LP'
        # self.status = 0
        self.animation_speed = .22
        # self.animation_list = self.load_images(sprite_sheet, animation_steps)
        # self.image = self.animation_list[self.status][self.frame_index]
        self.update_time = pg.time.get_ticks()  # spawn timestamp
        # self.rect = self.image.get_rect(topleft=(x,y))

        '''player state'''
        self.facing_right = True

    def import_character_assets(self):
        character_path = f'./assets/characters/{self.character}/'
        match self.character:
            case "Homusubi":
                self.animations = Homusubi_Anims
            case "Raijin":
                self.animations = Raijin_Anims

        for animation in self.animations.keys():
            full_path = character_path + animation
            original_images = import_folder(full_path)
            scaled_images = scale_images(
                original_images, (self.size, self.size))
            self.animations[animation] = scaled_images

    def animate(self):
        animation = self.animations[self.status]

		# loop over frame index
        if self.status != 'crouch':
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index -= 1
                if self.status == "idle":
                    self.frame_index = 0

                elif self.status == 'hit':
                    self.hit = False

                elif self.status == 'LP':
                    self.attacking = False
                    self.attack_cooldown = 3
                elif self.status == 'MP':
                    self.attacking = False
                    self.attack_cooldown = 3
                elif self.status == 'HP':
                    self.attacking = False
                    self.attack_cooldown = 3

                elif self.status == 'LK':
                    self.attacking = False
                    self.attack_cooldown = 3
                elif self.status == 'MK':
                    self.attacking = False
                    self.attack_cooldown = 3
                elif self.status == 'HK':
                    self.attacking = False
                    self.attack_cooldown = 3

                elif "2" not in self.status:
                    self.status = "idle"

                    '''CROUCHING NORMALS'''
                elif self.status == '2LP':
                    self.attacking = False
                    self.attack_cooldown = 3
                    self.update_action("crouch")
                    self.frame_index = 4
                elif self.status == '2MP':
                    self.attacking = False
                    self.attack_cooldown = 3
                    self.update_action("crouch")
                    self.frame_index = 4
                elif self.status == '2HP':
                    self.attacking = False
                    self.attack_cooldown = 3
                    self.update_action("crouch")
                    self.frame_index = 4


        if self.status == 'LP':
            self.frame_index += 0.2
        elif self.status == 'MP':
            self.frame_index += 0.1
        elif self.status == 'HP':
            self.frame_index += 0.2

        elif self.status == 'LK':
            self.frame_index += 0.2
        elif self.status == 'MK':
            self.frame_index += 0.2
        elif self.status == 'HK':
            self.frame_index += 0.2

        elif self.status == '2LP':
            self.frame_index += 0.4
        elif self.status == '2MP':
            self.frame_index += 0.1
        elif self.status == '2HP':
            self.frame_index += 0.1

        elif self.status == 'crouch':
            self.frame_index += self.animation_speed + 0.5
            for i in range(len(animation)):
                if self.frame_index >= len(animation):
                    self.frame_index -= 1

        self.image = animation[int(self.frame_index)]

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
          temp_img_list = []
          for x in range(animation):
            temp_img = sprite_sheet.subsurface(
                x * self.size, y, self.size, self.size)
            temp_img_list.append(pg.transform.scale(
                temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
          animation_list.append(temp_img_list)
        return animation_list

    def handle_keydowns(self, event, target):
        # check current action
        if not self.attacking and self.attack_cooldown == 0:
            '''ATTACKS'''
            # crouching normals
            if self.crouching:
                if event.key == LP:
                    self.attack_status = '2LP'
                    self.attack_type = 7
                    self.attacking = True
                elif event.key == MP:
                    self.attack_status = '2MP'
                    self.attack_type = 8
                    self.attacking = True
                elif event.key == HP:
                    self.attack_status = '2HP'
                    self.attacking = True
                    self.attack_type = 9
            
            # punches
            elif event.key == LP and self.on_ground:
                self.attack_status = 'LP'
                self.attack_type = 1
                self.attacking = True
            elif event.key == MP and self.on_ground:
                self.attack_status = 'MP'
                self.attack_type = 2
                self.attacking = True
            elif event.key == HP and self.on_ground:
                self.attack_status = 'HP'
                self.attack_type = 3
                self.attacking = True

            # kicks
            elif event.key == pg.K_k and self.on_ground:
                self.attack_status = 'LK'
                self.attack_type = 4
                self.attacking = True
            elif event.key == pg.K_l and self.on_ground:
                self.attack_status = 'MK'
                #if self.character == "Homusubi":
                    #self.rect.x += 40
                self.attack_type = 5
                self.attacking = True
            elif event.key == pg.K_SEMICOLON and self.on_ground:
                self.attack_status = 'HK'
                self.attack_type = 6
                self.attacking = True

            elif event.key == pg.K_LSHIFT and self.dir == "forward" and not self.dashing:
                print("FDASH")
                self.dashing = True
                self.rect.x += self.dashLength * 2
                self.rect.y -= 12
            elif event.key == pg.K_LSHIFT and self.dir == "back" and not self.dashing:
                print("BDASH")
                self.dashing = True
                self.rect.x -= (self.dashLength * 2)//2
                self.rect.y -= 12

            elif self.dashing:
                self.dX = 0

                if event.key == pg.K_w:
                    self.dY = 0
                if event.key == pg.K_a:
                    self.dX = 0
                if event.key == pg.K_d:
                    self.dX = 0
            
            if self.attacking:
                self.attacked = False

    def move(self, target):
        self.SPEED = 10
        self.dX = 0
        self.dY = 0
        self.walking = False
        key = pg.key.get_pressed()

        if not self.attacking and not self.throwing_proj:
            #movement
            if key[pg.K_a]:
                self.dir = "back"
                self.walking = True
                self.dX = - self.SPEED

                if self.mode == "Train":
                    self.arrow = Arrow(self.dir, self.arrow_locx, self.arrow_locy, self.arrow_size)

            if key[pg.K_d]:
                self.dir = "forward"
                self.walking = True
                self.dX = self.SPEED

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

                # text = FONT.render(f"{self.dir}", True, 'white', 'black')
                # textPos = text.get_rect(centerx = 100, y = 100)
                # pg.display.get_surface().blit(text, textPos)

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

                target.hp -= damage
                target.hit = True
                self.animated_text = TextAnimation("", 60, 0, target.hit_box.topright, "white",30,self.surface)
                self.animated_text.damage = damage
                self.super_meter += damage * 2
                self.proj = None
                self.fireball = False
                self.throwing_proj = False

        #check screen loc
        if self.rect.left + self.dX < 0:
            self.dX = -self.rect.left
        if self.rect.right + self.dX > screen_width:
            self.dX = screen_width - self.rect.right

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
        if self.rect.bottom + self.dY > screen_height - floor_height:
            self.on_ground = True
            self.vel_y = 0
            self.jumping = False
            self.dY = screen_height - floor_height - self.rect.bottom

        #update pos
        self.rect.x += self.dX
        self.rect.y += self.dY
        self.dashing = False

    def updateAnim(self, target):
        if self.hp <= 0:
           self.hp = 0
            #self.alive = False
            #self.update_action(6)
        elif self.hit == True:
            self.update_action('hit')
        
        elif self.attacking == True:

          '''ATTACK TYPES'''
          # NORMALS
          if self.attack_type == 1:
            self.update_action('LP')
          elif self.attack_type == 2:
            self.update_action('MP')
          elif self.attack_type == 3:
            self.update_action('HP')
          if self.attack_type == 4:
            self.update_action('LK')
          elif self.attack_type == 5:
            self.update_action('MK')
          elif self.attack_type == 6:
            self.update_action('HK')

          # CROUCH NORMALS
          elif self.attack_type == 7:
            self.update_action('2LP')
          elif self.attack_type == 8:
            self.update_action('2MP')
          elif self.attack_type == 9:
            self.update_action('2HP')
          elif self.attack_type == 10:
            self.update_action('2LK')
          elif self.attack_type == 11:
            self.update_action('2MK')
          elif self.attack_type == 12:
            self.update_action('2HK')


        elif self.jumping == True:
            self.update_action('jump')  #3:jump
        elif self.crouching == True:
            self.update_action('crouch')  #2: crouch
        elif self.walking == True:
            self.update_action('run')  #1:run
        else:
            self.update_action('idle')#0:idle

        if self.status in attacks and self.attack_type != 0 and not self.attacked:
            if int(self.frame_index) == hit_boxes["Homusubi"][str(self.attack_type)][0]:
                self.attacked = True
                self.attack(target)

    def update_action(self, new_status):
        #check if the new action is different to the previous one
        if new_status != self.status:
            self.status = new_status
            #update the animation settings
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    def attack(self, target):
        # get hitbox attributes for the active frame
        hitbox_attrs = hit_boxes["Homusubi"][str(self.attack_type)]
        offset_x, offset_y, w, h = hitbox_attrs[1]
        
        # calculate hitbox position using hitbox attributes and player rect
        flip_hit_box = self.rect.w
        if not self.facing_right:
            flip_hit_box *= -1
            offset_x = (offset_x * -1) - w
        x = self.hit_box.centerx + offset_x + flip_hit_box
        y = self.hit_box.centery + offset_y

        # create the hitbox from all the attributes together
        attack_rect = pg.Rect(x, y, w, h)
        # pg.draw.rect(pg.display.get_surface(), "green", attack_rect)

        # detect collision on the active frame
        if attack_rect.colliderect(target.hit_box) and not self.throwing_proj:
            target.hit = True
            self.super_meter += self.move_damage[self.attack_status] * 2
            target.hp -= self.move_damage[self.attack_status]
            self.hitspark(attack_rect, flip_hit_box)
            self.animated_text = TextAnimation("", 60, 0, target.hit_box.topright, "white",30,self.surface)
            self.animated_text.damage = self.move_damage[self.attack_status]

            # knockback
            if self.attacking:
                if self.facing_right:
                    self.rect.x -= 30
                else:
                    self.rect.x += 30

    def hitspark(self, attack_rect, flip_hit_box):
        # calculate hitspark position based on attack_rect
        offset_x = 40
        target_x = attack_rect.x
        if self.facing_right:
            offset_x *= -1
            target_x += flip_hit_box
        target_x += offset_x

        target_y = attack_rect.centery
        if self.crouching:
            target_y += 80

        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        self.particle.addParticles(target_x, target_y)
        # self.particle.update()    #call this to show hitspark animation
    
    def jump(self):
        self.dY += self.vel_y

    def applyGravity(self):
        self.vel_y += self.GRAVITY
    
    def applyGravityDash(self):
        self.vel_y += self.dashGravity

    def getInputs(self, char:str):
        match char:
            case "Homusubi":
                self.inputs = Subi_Inputs.copy()
                self.inputValues = list(self.inputs.values())
                self.inputKey = list(self.inputs.keys())
            case "Raijin":
                self.inputs = Raijin_Inputs.copy()
                self.inputValues = list(self.inputs.values())
                self.inputKey = list(self.inputs.keys())

    def checkMoveCombo(self):
        moveCombo = self.moveCombo
        if not self.facing_right:
            moveCombo = [pg.K_a if key == pg.K_d else pg.K_d if key == pg.K_a else key for key in moveCombo]

        for i in range(len(self.inputValues)):
            if self.proj is None:

                if moveCombo == list(self.inputValues[0]):
                    self.proj = Projectile("FSTECH", "LFB", 98, (self.rect.centerx, self.rect.y), self, self.facing_right)
                    self.fireball = True

                if moveCombo == list(self.inputValues[1]):
                    self.proj = Projectile("FSTECH", "MFB", 98, (self.rect.centerx, self.rect.y), self, self.facing_right)
                    self.fireball = True

                if moveCombo == list(self.inputValues[2]):
                    self.proj = Projectile("FSTECH", "HFB", 98, (self.rect.centerx, self.rect.y), self, self.facing_right)
                    self.fireball = True

                if self.fireball and self.proj is not None:
                    self.proj.frames_passed = 0
                    self.throwing_proj = True
                    self.moveCombo = []

                elif self.fireball:
                    self.fireball = False
                    self.throwing_proj = False

    def draw(self):
        pg.key.set_repeat(0)
        self.particle.emit("white")
        if self.dashing:
            self.applyGravityDash()
        else:
            self.applyGravity()
        if self.proj is not None:
            if self.facing_right:
                self.proj.move()
                self.proj.draw(pg.display.get_surface())
            if not self.facing_right:
                self.proj.move()
                self.proj.draw(pg.display.get_surface())

        self.animate()
        self.getInputs(self.character)
        if self.moveCombo:
            self.checkMoveCombo()
        self.hit_box = pg.Rect(self.rect.x, self.rect.y - 100, 120, 280)
        img = pg.transform.flip(self.image, self.flip, False)
        # pg.draw.rect(self.surface,"red",self.rect)
        # pg.draw.rect(self.surface,"blue",self.hit_box)

        if self.flip:
            self.surface.blit(img,(self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        else:
            self.surface.blit(img,(self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

        if self.super_meter > 250:
            self.super_meter = 250
