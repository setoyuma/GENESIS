import pygame as pg
import sys
import json

from fighter import Fighter
from particle import ParticlePrinciple
from color_animation import ColorGradient
from button import Button
from slider import Slider
from settings import * 
from support import *
from character_variables import *

# br ~ tr ~ tl ~ bl  br=0                          # tr=3     # tl=4               # bl=6
blast_points = [(179, 127), (195, 99), (225, 98), (225, 95), (30, 85), (6, 113), (28, 137), (53, 123), (92, 112), (173, 127)]
right_blast_points = [(1421, 127), (1405, 99), (1375, 98), (1375, 95), (1570, 85), (1594, 113), (1572, 137), (1547, 123), (1508, 112), (1427, 127)]
top_points = [(30, 85), (6, 113)]
bottom_points = [(225, 95), (53, 123)]
y_distances = [point[1] - top_points[i][1] for i, point in enumerate(bottom_points)]
health_bar_colors = ColorGradient((0,255,0), (255,0,0)).generate_gradient()

class Game:
	def __init__(self):
		pg.init()
		self.load_settings()

		# music and sound
		pg.mixer.init()
		pg.mixer.music.load(self.settings["songs"]['main'])
		pg.mixer.music.play(-1)
		self.volume = 0.25
		pg.mixer.music.set_volume(self.volume)

		# display
		self.screen = pg.display.set_mode((self.settings["screen_width"], self.settings["screen_height"]), )
		self.clock = pg.time.Clock()
		pg.display.set_icon(pg.image.load('./assets/icons/main/gameicon.ico'))
		pg.display.set_caption("Kami No Ken: GENESIS")

		# background animation
		self.import_assets()
		self.frame_index = 0
		self.bg = self.settings["backgrounds"]["ogre"]
		# self.image = self.bg_animations[self.bg][self.frame_index]
		self.animation_speed = 0.25

	def load_settings(self):
		
		reader = open('settings.json', 'r')
		self.settings = json.loads(reader.read())
		

		# data = json.load(reader)
		# print(data)
		# print(settings["self.settings["FPS"]"])

		HALF_SCREENW = self.settings["screen_width"]//2
		HALF_SCREENH = self.settings["screen_height"]//2
		QUARTER_SCREENW = self.settings["screen_width"]//4
		QUARTER_SCREENH = self.settings["screen_width"]//4
		
		'''MOVEMENT'''
		UP = pg.K_w
		DOWN = pg.K_s
		BACK = pg.K_a
		FORWARD = pg.K_d

		'''ATTACKS'''
		LP = pg.K_i
		MP = pg.K_o
		HP = pg.K_p
		LK = pg.K_k
		MK = pg.K_l
		HK = pg.K_SEMICOLON

	def import_assets(self):
		# hud
		HUD = get_image("./assets/ui/HUD/HUD.png")
		self.scaled_HUD = pg.transform.scale(HUD, (self.settings["screen_width"],  self.settings["screen_height"]/3))

		# portait
		# will need to change eventually for new characters
		portrait = get_image(f"./assets/characters/Homusubi/portrait/portrait.png")
		size = 80
		self.scaled_portrait = pg.transform.scale(portrait, (size+20, size-10))

		# bg
		self.bg_animations = { "bay-side-carnival": [], "ogre-gate": []}
		bg_path = f'./assets/backgrounds/'

		for animation in self.bg_animations.keys():
			full_path = bg_path + animation
			original_images = import_folder(full_path)
			scaled_images = scale_images(original_images, (self.settings["screen_width"], self.settings["screen_height"]))
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
		surf.blit(self.scaled_HUD, (0,-55))

	def drawHealthBar(self, target):
		# percentage of hp
		ratio = target.hp / 200

		# determines color in the gradient list
		color_index = len(health_bar_colors) - int(ratio * len(health_bar_colors))
		if color_index >= len(health_bar_colors):
			color_index = len(health_bar_colors) - 1

		# player 1
		if target == self.player_1:
			super_meter_gain = (self.player_1.super_meter / 250) * .68
			#health meter
			pg.draw.polygon(self.screen, health_bar_colors[color_index], [(30+(600*ratio), 85+(ratio*27)), (30+(600*ratio), 67-(ratio*27)), (30, 65), (30, 85)])
			#super meter
			pg.draw.polygon(self.screen, "red", [(190 + (super_meter_gain * 635), 113 + (super_meter_gain * 54)), (200 + (super_meter_gain * 615), 93 + (super_meter_gain * 26)), (200 , 93), (190, 113)])
			# blast meter
			if self.player_1.super_meter >= 50: # and self.player_1.blast_cooldown == 0:
				#adjusted_points = [(point[0], point[1] - 20) for i, point in enumerate(blast_points) if i in top_blast_points]
				pg.draw.polygon(self.screen, "yellow", blast_points)
		
		# player 2
		else:
			left_x = self.settings["screen_width"] - 610
			right_x = self.settings["screen_width"] - 33
			#health meter
			pg.draw.polygon(self.screen, health_bar_colors[color_index], [(right_x-(600*ratio), 85+(ratio*27)), (right_x-(600*ratio), 67-(ratio*27)), (right_x, 65), (right_x, 85)])
			#super meter
			pg.draw.polygon(self.screen, "blue", [(self.settings["screen_width"] - 635, 148), (self.settings["screen_width"] - 615, 110), (self.settings["screen_width"] - 200, 93), (self.settings["screen_width"] - 190, 113)])
			# blast meter
			if self.player_2.super_meter >= 50: # and self.player_1.blast_cooldown == 0:
				#adjusted_points = [(point[0], point[1] + (ratio * y_distances[top_points.index(point)])) if point in top_points else point for point in blast_points]
				pg.draw.polygon(self.screen, "yellow", right_blast_points)

	def draw_portrait(self, target):
		portrait = self.scaled_portrait

		if target ==  self.player_1:
			pos = (50, 2)

		else:
			pos = (1460, 2)
			portrait = pg.transform.flip(portrait, True, False)

		self.screen.blit(portrait, pos)

	def send_frame(self):
		self.dt = self.clock.tick(self.settings["FPS"])/2000
		pg.display.flip()

	def MainMenu(self):
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		play_button = Button(self.settings["screen_width"]/2, self.settings["screen_height"]/2, 200, 100, "PLAY", self.HomeScreen)
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)

		while True:
			self.screen.fill('black')
			self.screen.blit(mainMenuBG,(480,115))

			for event in pg.event.get():
				check_for_quit(event)
				
				if event.type == PARTICLE_EVENT:
					mouse_pos = pg.mouse.get_pos()
					particle1.addParticles(mouse_pos[0], mouse_pos[1])
				
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_SPACE:
						self.Play()

				play_button.Process(event)

			play_button.draw()
			particle1.emit()
			self.send_frame()

	def SoundSettings(self):
		pg.display.set_caption("Kami No Ken: SOUND SETTINGS")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)
		slider = Slider(self.settings["screen_width"]/2 - 95, 145, 200, 10, self.volume)
		volume_button = Button(self.settings["screen_width"]/2, 40, 200, 100, "VOLUME", None)
		back_button = Button(self.settings["screen_width"]/2, 160, 200, 100, "BACK", self.Options)

		while True:
			self.screen.fill('black')
			self.screen.blit(mainMenuBG,(480,115))

			slider.draw(self.screen)

			mouse_pos = pg.mouse.get_pos()
			if slider.active:
				slider.handle_event(self.screen, mouse_pos[0])
				self.volume = slider.get_volume()
				pg.mixer.music.set_volume(self.volume / 100)

			for event in pg.event.get():
				check_for_quit(event)
				
				if event.type == PARTICLE_EVENT:
					mouse_pos = pg.mouse.get_pos()
					particle1.addParticles(mouse_pos[0], mouse_pos[1])
				
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_SPACE:
						self.Play()

				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and slider.on_slider(mouse_pos[0], mouse_pos[1]):
					#slider.on_slider_hold(mouse_pos[0], mouse_pos[1])
					slider.active = True
					slider.handle_event(self.screen, mouse_pos[0])
					self.volume = slider.get_volume()
					pg.mixer.music.set_volume(self.volume/100)

				elif event.type == pg.MOUSEBUTTONUP:
					slider.active = False
			
				volume_button.Process(event)
				back_button.Process(event)

			volume_button.draw()
			back_button.draw()

			particle1.emit()
			self.send_frame()

	def HomeScreen(self):
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)

		fight_button = Button(70, 40, 200, 100, "LOCAL", self.PlayLocal)
		train_button = Button(70, 120, 200, 100, "TRAINING", self.Training)
		back_button = Button(70, 200, 200, 100, "BACK", self.MainMenu)
		options_button = Button(70, 280, 200, 100, "OPTIONS", self.Options)

		while True:
			self.screen.fill('black')
			self.screen.blit(mainMenuBG,(480,115))

			for event in pg.event.get():
				check_for_quit(event)
	
				if event.type == PARTICLE_EVENT:
					mouse_pos = pg.mouse.get_pos()
					particle1.addParticles(mouse_pos[0], mouse_pos[1])
				
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_SPACE:
						self.Play()
            
				back_button.Process(event)
				fight_button.Process(event)
				train_button.Process(event)
				options_button.Process(event)

			back_button.draw()
			fight_button.draw()
			train_button.draw()
			options_button.draw()

			particle1.emit()
			self.send_frame()
	
	def Options(self):
		pg.display.set_caption("Kami No Ken: OPTIONS")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)
		back_button = Button(self.settings["screen_width"]//2, 480, 200, 100, "BACK", self.HomeScreen)
		sound_button = Button(self.settings["screen_width"]//2, 320, 200, 100, "SOUND", self.SoundSettings)
		video_button = Button(self.settings["screen_width"]//2, 400, 200, 100, "VIDEO", self.HomeScreen)

		while True:
			self.screen.fill('black')
			self.screen.blit(mainMenuBG,(480,115))

			for event in pg.event.get():
				check_for_quit(event)
	
				if event.type == PARTICLE_EVENT:
					mouse_pos = pg.mouse.get_pos()
					particle1.addParticles(mouse_pos[0], mouse_pos[1])
				
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_SPACE:
						self.Play()
            
				sound_button.Process(event)
				video_button.Process(event)
				back_button.Process(event)

			sound_button.draw()
			video_button.draw()
			back_button.draw()

			particle1.emit()
			self.send_frame()
	
	def Training(self):
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(self.settings["songs"]['credits'])
		pg.mixer.music.play(-1)
		pg.mixer.music.set_volume(0.1)

		self.player_1 = Fighter(self, 200, 510, False, "Homusubi", "Train")
		self.player_2 = Fighter(self, 1000, 570, True, "Homusubi", "Train")

		while True:

			self.screen.fill('grey')
			self.animate()
			self.drawBG()

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
				check_for_quit(event)

				if event.type == pg.KEYDOWN:
					self.player_1.handle_keydowns(event, self.player_2)
					self.player_1.moveCombo.append(event.key)
					# self.player_2.moveCombo.append(event.key)

					if event.key == pg.K_r:
						self.__init__()
						self.MainMenu()

					elif event.key == pg.K_h:
						pg.draw.rect(self.screen, "green", self.player_1.hit_box)

					elif event.key == pg.K_RSHIFT:
						pass

			#show player stats
			self.drawHealthBar(self.player_1)
			self.drawHealthBar(self.player_2)

			self.draw_HUD(self.screen)

			self.draw_portrait(self.player_1)
			self.draw_portrait(self.player_2)

			# show self.settings["fps"]
			fpsCounter = round(self.clock.get_fps())
			draw_text(self.screen, f"FPS: {fpsCounter}", (self.settings["screen_width"]/2, 200))

			self.send_frame()
	
	def Play(self):
		pass
	
	def Test(self):
		# self.load_settings()
		UP = pg.K_w
		DOWN = pg.K_s
		BACK = pg.K_a
		FORWARD = pg.K_d

		'''ATTACKS'''
		LP = pg.K_i
		MP = pg.K_o
		HP = pg.K_p
		LK = pg.K_k
		MK = pg.K_l
		HK = pg.K_SEMICOLON

		print(HK)
	
	def PlayLocal(self):
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(self.settings["songs"]['science'])
		pg.mixer.music.play(-1)

		self.player_1 = Fighter(self, 200, 510, False, "Homusubi", self.dt)
		self.player_2 = Fighter(self, 1000, 570, True, "Homusubi", self.dt)

		COUNT_DOWN = pg.USEREVENT + 1
		self.match_time = 99

		while True:

			self.screen.fill('grey')
			self.animate()
			self.drawBG()

			'''PLAYER MVMNT'''
			self.player_1.move(self.player_2)
			#self.dummy.move(self.player_1)

			#update fighters
			self.player_1.updateAnim(self.player_2)
			self.player_2.updateAnim(self.player_1)

			self.player_1.framesWithoutCombo += 1
			if self.player_1.framesWithoutCombo > 26 or len(self.player_1.moveCombo) > 9:
				self.player_1.framesWithoutCombo = 0
				self.player_1.moveCombo = []

			for event in pg.event.get():
				check_for_quit(event)

				if event.type == COUNT_DOWN:
					dt = self.dt
					self.match_time -= dt
					self.match_time_text = str(int(self.match_time)).rjust(3) if int(self.match_time) > 0 else 'GAME'
					if int(self.match_time) == 0:
						self.match_time = 0
						print("match over")

				if event.type == pg.KEYDOWN:
					self.player_1.handle_keydowns(event, self.player_2)
					self.player_1.moveCombo.append(event.key)
					# self.player_2.moveCombo.append(event.key)

					if event.key == pg.K_r:
						self.__init__()
						self.MainMenu()

					if event.key == pg.K_h:
						pg.draw.rect(self.screen, "green", self.player_1.hit_box)

					if event.key == pg.K_RSHIFT:
						pass

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
			self.drawHealthBar(self.player_1)
			self.drawHealthBar(self.player_2)

			self.draw_HUD(self.screen)

			self.draw_portrait(self.player_1)
			self.draw_portrait(self.player_2)

			
			# match clock
			draw_text(self.screen, self.match_time_text[:-1], (self.settings["screen_width"]/2 - 70, 80), 100, (255, 0, 0))
			draw_text(self.screen, self.match_time_text[-1:], (self.settings["screen_width"]/2 + 50, 80), 100, (255, 0, 0))

			# show self.settings["fps"]
			fpsCounter = round(self.clock.get_fps())
			draw_text(self.screen, f"FPS: {fpsCounter}", (self.settings["screen_width"]/2, 200))

			self.send_frame()

if __name__ == '__main__':
	game = Game()
	# game.Test()
	game.MainMenu()