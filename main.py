import pygame as pg
import sys

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

		# music and sound
		pg.mixer.init()
		pg.mixer.music.load(songs['main'])
		pg.mixer.music.play(-1)
		self.volume = 0.25
		pg.mixer.music.set_volume(self.volume)

		# display
		self.screen = pg.display.set_mode((screen_width, screen_height), )
		self.clock = pg.time.Clock()
		pg.display.set_icon(pg.image.load('./assets/icons/main/gameicon.ico'))
		pg.display.set_caption("Kami No Ken: GENESIS")

		# background animation
		self.import_assets(carnival)
		self.frame_index = 0
		self.bg = carnival
		self.image = self.bg_animations[self.bg][self.frame_index]
		self.animation_speed = 0.25

	def import_assets(self, bg):
		# hud
		HUD = get_image("./assets/ui/HUD/HUD.png")
		self.scaled_HUD = pg.transform.scale(HUD, (screen_width,  screen_height/3))

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
			left_x = screen_width - 610
			right_x = screen_width - 33
			#health meter
			pg.draw.polygon(self.screen, health_bar_colors[color_index], [(right_x-(600*ratio), 85+(ratio*27)), (right_x-(600*ratio), 67-(ratio*27)), (right_x, 65), (right_x, 85)])
			#super meter
			pg.draw.polygon(self.screen, "blue", [(screen_width - 635, 148), (screen_width - 615, 110), (screen_width - 200, 93), (screen_width - 190, 113)])
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
		self.clock.tick(FPS)
		pg.display.flip()

	def MainMenu(self):
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		play_button = Button(screen_width//2,screen_height//2,200,100,"PLAY",self.HomeScreen,True)
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

			play_button.Process()
			particle1.emit("Red")
			self.send_frame()

	def SoundSettings(self):
		pg.display.set_caption("Kami No Ken: SOUND SETTINGS")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)
		slider = Slider(screen_width//2 - 95, 145, 200, 10, self.volume)
		volume_button = Button(screen_width//2, 40, 200, 100, "VOLUME", None, True)
		back_button = Button(screen_width//2, 160, 200, 100, "BACK", self.Options, True)

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
			
			volume_button.Process()
			back_button.Process()
			particle1.emit("Red")
			self.send_frame()

	def HomeScreen(self):
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)

		fight_button = Button(70, 40, 200, 100, "LOCAL", self.PlayLocal, True)
		train_button = Button(70, 120, 200, 100, "TRAINING", self.Training, True)
		back_button = Button(70, 200, 200, 100, "BACK", self.MainMenu, True)
		options_button = Button(70, 280, 200, 100, "OPTIONS", self.Options, True)

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
            
			back_button.Process()
			fight_button.Process()
			train_button.Process()
			options_button.Process()
			particle1.emit("Red")
			self.send_frame()
	
	def Options(self):
		pg.display.set_caption("Kami No Ken: OPTIONS")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)

		while True:
			self.screen.fill('black')
			self.screen.blit(mainMenuBG,(480,115))
			sound_button = Button(screen_width//2,320,200,100,"SOUND",self.SoundSettings,True)
			video_button = Button(screen_width//2,400,200,100,"VIDEO",self.HomeScreen,True)
			back_button = Button(screen_width//2, 480, 200, 100, "BACK", self.HomeScreen, True)

			for event in pg.event.get():
				check_for_quit(event)
	
				if event.type == PARTICLE_EVENT:
					mouse_pos = pg.mouse.get_pos()
					particle1.addParticles(mouse_pos[0], mouse_pos[1])
				
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_SPACE:
						self.Play()
            
			sound_button.Process()
			video_button.Process()
			back_button.Process()
			particle1.emit("Red")
			self.send_frame()
	
	def Training(self):
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(songs['credits'])
		pg.mixer.music.play(-1)
		pg.mixer.music.set_volume(0.1)

		self.player_1 = Fighter(self, 200, 510, False, "Homusubi", "Train")
		self.player_2 = Fighter(self, 1000, 570, True, "Homusubi", "Train")

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

			# show fps
			fpsCounter = round(self.clock.get_fps())
			draw_text(self.screen, f"FPS: {fpsCounter}", (HALF_SCREENW, 200))

			self.send_frame()
	
	def Play(self):
		pass
	
	def PlayLocal(self):
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(songs['science'])
		pg.mixer.music.play(-1)

		self.player_1 = Fighter(self, 200, 510, False, "Homusubi")
		self.player_2 = Fighter(self, 1000, 570, True, "Homusubi")
		while True:

			self.screen.fill('grey')
			self.drawBG()
			self.animate()

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

			# show fps
			fpsCounter = round(self.clock.get_fps())
			draw_text(self.screen, f"FPS: {fpsCounter}", (HALF_SCREENW, 200))

			self.send_frame()

if __name__ == '__main__':
	game = Game()
	game.MainMenu()