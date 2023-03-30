import pygame as pg
import sys

from fighter import Fighter
from button import Button
from particle import ParticlePrinciple
from settings import * 
from support import *
from character_variables import *

# might need to pre-init mixer to reduce sound delay (will affect sound effects)

class Game:
	def __init__(self):
		# pg setup
		pg.init()
		pg.key.set_repeat(0)
		pg.mixer.init()
		pg.mixer.music.load(songs['main'])
		pg.mixer.music.play(-1)
		pg.mixer.music.set_volume(0.0)
		self.screen = pg.display.set_mode((screen_width, screen_height), )
		self.bg_animations = { "bay-side-carnival": [], "ogre-gate": []}
		pg.display.set_caption("Kami No Ken: GENESIS")
		self.import_assets(carnival)
		self.clock = pg.time.Clock()
		self.frame_index = 0
		self.bg = carnival
		self.image = self.bg_animations[self.bg][self.frame_index]
		self.animation_speed = 0.25

	def import_assets(self, bg):
		bg_path = f'./assets/backgrounds/'

		for animation in self.bg_animations.keys():
			full_path = bg_path + animation
			original_images = import_folder(full_path)
			scaled_images = scale_images(original_images, (screen_width, screen_height))
			self.bg_animations[animation] = scaled_images

	def animate(self):
		animation = self.bg_animations[self.bg]
        
		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		self.image = image

	def drawBG(self):
		self.screen.blit(self.image,(0,0))

	def draw_HUD(self, surf):
		HUD = get_image("./assets/ui/HUD/In-Battle-HUD2.png")
		scaled_HUD = pg.transform.scale(HUD, (screen_width,  screen_height/3))
		# surf.blit(HUD, (400,0))
		surf.blit(scaled_HUD, (0,-55))

	def drawHealthBar(self, hp, x, y):
		health_bar_colors = {
			"Green 1" : "#00980b",
			"Green 2" : "#57bf00" ,
			"Green 3" : "#a1ff00" ,
			"Yellow 1" : "#fff700" ,
			"Yellow 2" : "#ffbf00" ,
			"Orange 1" : "#ff9d00" ,
			"Orange 2" : "#ff4f00",
			"Red 1" : "#ff0000" ,
		}

		# player 1
		ratio = self.player_1.hp / 200
		pg.draw.polygon(self.screen, health_bar_colors["Red 1"], [(610, 112), (610, 40), (30, 65), (30, 85)])  # br, tr, tl, bl
		pg.draw.polygon(self.screen, health_bar_colors["Green 1"], [(30+(600*ratio), 85+(ratio*27)), (30+(600*ratio), 67-(ratio*27)), (30, 65), (30, 85)])
		pg.draw.polygon(self.screen, "#ff0000", [(635, 148), (615, 110), (200, 93), (190, 113)])

		# player 2
		ratio = self.player_2.hp / 200
		print(ratio)
		left_x = HALF_SCREENW + (HALF_SCREENW - 610)
		right_y = screen_width - 30
		pg.draw.polygon(self.screen, health_bar_colors["Red 1"], [(left_x, 112), (left_x, 40), (right_y, 65), (right_y, 85)])
		pg.draw.polygon(self.screen, health_bar_colors["Green 1"], [((left_x/ratio), 85+(ratio*27)), ((left_x/ratio), 67-(ratio*27)), (right_y, 65), (right_y, 85)])
		#pg.draw.polygon(self.screen, "orange", [(635, 148), (615, 110), (200, 93), (190, 113)])

	def draw_portrait(self, x, y, size, target, surf):
		portrait = get_image(f"./assets/characters/{target.character}/portrait/portrait.png")
		scaled_portrait = pg.transform.scale(portrait, (size+20, size-10))
		surf.blit(scaled_portrait, (x,y))
		pass

	def MainMenu(self):
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)

		while True:
			self.screen.fill('black')
			self.screen.blit(mainMenuBG,(480,115))
			play_button = Button(screen_width//2,screen_height//2,200,100,"PLAY",self.HomeScreen,True)
			for event in pg.event.get():
				if event.type == pg.QUIT:
						print('\nGame Closed\n')
						pg.quit()
						sys.exit()
				if event.type == PARTICLE_EVENT:
					particle1.addParticles(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_q:
						print('\nGame Closed\n')
						pg.quit()
						sys.exit()
					if event.key == pg.K_SPACE:
						self.Play()
            
			play_button.Process()
			self.clock.tick(60)
			particle1.emit("Red")
			pg.display.flip()
	
	def Options(self):
		pg.display.set_caption("Kami No Ken: OPTIONS")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)

		while True:
			self.screen.fill('black')
			self.screen.blit(mainMenuBG,(480,115))
			sound_button = Button(screen_width//2,400,200,100,"SOUND",self.HomeScreen,True)
			video_button = Button(screen_width//2,480,200,100,"VIDEO",self.HomeScreen,True)
			for event in pg.event.get():
				if event.type == pg.QUIT:
						print('\nGame Closed\n')
						pg.quit()
						sys.exit()
				if event.type == PARTICLE_EVENT:
					particle1.addParticles(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_q:
						print('\nGame Closed\n')
						pg.quit()
						sys.exit()
					if event.key == pg.K_SPACE:
						self.Play()
            
			sound_button.Process()
			video_button.Process()
			self.clock.tick(60)
			particle1.emit("Red")
			pg.display.flip()
	
	def HomeScreen(self):
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)

		while True:
			self.screen.fill('black')
			self.screen.blit(mainMenuBG,(480,115))
			fight_button = Button(70, 40, 200, 100, "LOCAL", self.PlayLocal, True)
			train_button = Button(70, 120, 200, 100, "TRAINING", self.Training, True)
			back_button = Button(70, 200, 200, 100, "BACK", self.MainMenu, True)
			options_button = Button(70, 280, 200, 100, "OPTIONS", self.Options, True)
			for event in pg.event.get():
				if event.type == pg.QUIT:
						print('\nGame Closed\n')
						pg.quit()
						sys.exit()
				if event.type == PARTICLE_EVENT:
					particle1.addParticles(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_q:
						print('\nGame Closed\n')
						pg.quit()
						sys.exit()
					if event.key == pg.K_SPACE:
						self.Play()
            
			back_button.Process()
			fight_button.Process()
			train_button.Process()
			options_button.Process()
			self.clock.tick(60)
			particle1.emit("Red")
			pg.display.flip()

	def Training(self):
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(songs['credits'])
		pg.mixer.music.play(-1)
		pg.mixer.music.set_volume(0.1)

		self.player_1 = Fighter(self, 200, 510, False, self.screen, "Homusubi", subi_data, subi_sheet, subi_anim_steps, "Train")
		self.player_2 = Fighter(self, 1000, 570, True, self.screen, "Homusubi", subi_data, subi_sheet, subi_anim_steps, "Train")

		while True:

			self.screen.fill('grey')
			self.drawBG()
			self.animate()

			'''PLAYER MVMNT'''
			self.player_1.move(self.player_2)
			# self.player_2.move(self.player_1)


			#update fighters
			self.player_1.updateAnim(self.player_2)
			self.player_2.updateAnim(self.player_1)
			
			'''DRAW PLAYER'''
			self.player_2.draw()
			self.player_1.draw()

			

			self.player_1.framesWithoutCombo += 1
			if self.player_1.framesWithoutCombo > 26 or len(self.player_1.moveCombo) > 9:
				self.player_1.framesWithoutCombo = 0
				self.player_1.moveCombo = []

			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()
				if event.type == pg.KEYDOWN:
					self.player_1.handle_keydowns(event, self.player_2)
					self.player_1.moveCombo.append(event.key)
					# self.player_2.moveCombo.append(event.key)
					if event.key == pg.K_q:
						pg.quit()
						sys.exit()
					if event.key == pg.K_r:
						self.__init__()
						self.MainMenu()
					if event.key == pg.K_RSHIFT:
						pass
					if event.key == pg.K_h:
						pg.draw.rect(self.screen, "green", self.player_1.hit_box)
					
			
			'''DISPLAY STATS'''
			# #p1
			#draw_text(self.screen, f"{self.player_1.hp}", (100, 100), 30, (255,0,0))
			
			# #p2
			#draw_text(self.screen, f"{self.player_2.hp}", (1500, 40), 30, (255,0,0))

			
			#show player stats
			self.drawHealthBar(self.player_1.hp, 40, 48)
			self.drawHealthBar(self.player_2.hp, screen_width - 608, 48)
			self.draw_HUD(self.screen)

			# show fps
			fpsCounter = str(int(self.clock.get_fps()))
			draw_text(self.screen, f"FPS: {fpsCounter}", (1000, 10))

			pg.display.update()
			self.clock.tick(FPS)
	
	def Play(self):
		pass
	
	def PlayLocal(self):
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(songs['science'])
		pg.mixer.music.play(-1)
		pg.mixer.music.set_volume(0.0)

		self.player_1 = Fighter(self, 200, 510, False, self.screen, "Homusubi", subi_data, subi_sheet, subi_anim_steps, "Play")
		self.player_2 = Fighter(self, 1000, 570, True, self.screen, "Homusubi", subi_data, subi_sheet, subi_anim_steps, "Play")

		while True:

			self.screen.fill('grey')
			self.drawBG()
			self.animate()


			'''PLAYER MVMNT'''
			self.player_1.move(self.player_2)
			# self.dummy.move(self.player_1)

			#update fighters
			self.player_1.updateAnim(self.player_2)
			self.player_2.updateAnim(self.player_1)


			self.player_1.framesWithoutCombo += 1
			if self.player_1.framesWithoutCombo > 26 or len(self.player_1.moveCombo) > 9:
				self.player_1.framesWithoutCombo = 0
				self.player_1.moveCombo = []

			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()
				if event.type == pg.KEYDOWN:
					self.player_1.handle_keydowns(event, self.player_2)
					self.player_1.moveCombo.append(event.key)
					# self.player_2.moveCombo.append(event.key)
					if event.key == pg.K_q:
						pg.quit()
						sys.exit()
					if event.key == pg.K_r:
						self.__init__()
						self.MainMenu()
					if event.key == pg.K_RSHIFT:
						pass
					if event.key == pg.K_h:
						pg.draw.rect(self.screen, "green", self.player_1.hit_box)
					
			
			'''DISPLAY STATS'''
			# #p1
			#draw_text(self.screen, f"{self.player_1.hp}", (100, 100), 30, (255,0,0))
			
			# #p2
			#draw_text(self.screen, f"{self.player_2.hp}", (1500, 40), 30, (255,0,0))

			'''DRAW PLAYER'''
			self.player_2.draw()
			self.player_1.draw()
			
			if self.player_1.animated_text is not None:
				if self.player_1.animated_text.update():
					self.player_1.animated_text = None
			if self.player_2.animated_text is not None:
				if self.player_2.animated_text.update():
					self.player_2.animated_text = None
			
			#show player stats
			self.drawHealthBar(self.player_1.hp, 40, 48)
			self.draw_HUD(self.screen)
			self.draw_portrait(50, 0, 80, self.player_1, self.screen)
			self.draw_portrait(1500, 0, 80, self.player_2, self.screen)

			# show fps
			fpsCounter = str(int(self.clock.get_fps()))
			draw_text(self.screen, f"FPS: {fpsCounter}", (1000, 10))

			pg.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.MainMenu()