import pygame as pg

import json
from support import *
from scene import Scene
from button import Button
from particle import ParticlePrinciple
from slider import Slider
from constants import *
from fighter import Fighter

class Main_Menu(Scene):
	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		self.bg = get_image("./assets/backgrounds/main-menu/KnK.png")
		self.buttons = [
			Button(self.game, "PLAY", (self.game.settings["screen_width"]/2, self.game.settings["screen_height"]/2), Home_Screen, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			
			Button(self.game, "QUIT", (self.game.settings["screen_width"] - 100, 50,), pg.quit, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30)
		]

		# mouse fx
		self.accumulator = 0
		self.particle1 = ParticlePrinciple()

	def update(self):
		if self.accumulator >= 5 / 1000:
			mouse_pos = pg.mouse.get_pos()
			self.particle1.addParticles(mouse_pos[0], mouse_pos[1])
			self.accumulator = 0

		pressed_keys = pg.key.get_pressed()
		for event in pg.event.get():
			self.check_universal_events(pressed_keys, event)

			for button in self.buttons:
				button.update(event)

	def draw(self):
		self.game.screen.fill('black')
		self.game.screen.blit(self.bg, (480,115))
		for button in self.buttons:
			button.draw()

		self.particle1.emit()
		self.game.send_frame()
		self.accumulator += self.game.dt

class Sound_Settings(Scene):
	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: SOUND")
		self.bg = get_image("./assets/backgrounds/main-menu/KnK.png")
		self.volume = self.game.settings["game_volume"]
		self.slider = Slider(self.game.settings["screen_width"]/2 - 95, 145, 200, 10, self.volume)
		self.buttons = [
			Button(self.game, "VOLUME", (self.game.settings["screen_width"]//2, 40), None, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			Button(self.game, "BACK", (self.game.settings["screen_width"]//2, 260), Options, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			
		]
		# mouse fx
		self.accumulator = 0
		self.particle1 = ParticlePrinciple()

	def update(self):
		mouse_pos = pg.mouse.get_pos()
		
		if self.slider.active:
			self.slider.handle_event(self.game.screen, mouse_pos[0])
			self.volume = self.slider.get_volume()
			pg.mixer.music.set_volume(self.volume / 100)

		if self.accumulator >= 5 / 1000:
			self.particle1.addParticles(mouse_pos[0], mouse_pos[1])
			self.accumulator = 0

		pressed_keys = pg.key.get_pressed()
		for event in pg.event.get():
			self.check_universal_events(pressed_keys, event)

			if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.slider.on_slider(mouse_pos[0], mouse_pos[1]):
				#slider.on_slider_hold(mouse_pos[0], mouse_pos[1])
				self.slider.active = True
				self.slider.handle_event(self.game.screen, mouse_pos[0])
				self.volume = self.slider.get_volume()
				pg.mixer.music.set_volume(self.volume/100)
			
			elif event.type == pg.MOUSEBUTTONUP:
				self.slider.active = False

			for button in self.buttons:
				button.update(event)

	def draw(self):
		self.game.screen.fill('black')
		self.game.screen.blit(self.bg, (480,115))
		for button in self.buttons:
			button.draw()
		self.slider.draw(self.game.screen)
		self.particle1.emit()
		self.game.send_frame()
		self.accumulator += self.game.dt

class Home_Screen(Scene):
	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: HOME")
		self.bg = get_image("./assets/backgrounds/main-menu/KnK.png")
		self.buttons = [
			Button(game, "LOCAL",(70,40), Local_Play,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			# Button(game, "ONLINE",(70,120), self.game.lobby_view,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			Button(game, "BACK",(70,200), Main_Menu,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			Button(game, "OPTIONS",(70,280), Options,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			# Button(game, "TRAINING",(70,360), self.game.training,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			Button(game, "QUIT",(self.game.settings["screen_width"] - 100 , 50), pg.quit,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			#Button(self, 70, 120, 200, 100, 30, "TRAINING", self.training),
		]

		# mouse fx
		self.accumulator = 0
		self.particle1 = ParticlePrinciple()

	def update(self):
		if self.accumulator >= 5 / 1000:
			mouse_pos = pg.mouse.get_pos()
			self.particle1.addParticles(mouse_pos[0], mouse_pos[1])
			self.accumulator = 0

		pressed_keys = pg.key.get_pressed()
		for event in pg.event.get():
			self.check_universal_events(pressed_keys, event)

			for button in self.buttons:
				button.update(event)

	def draw(self):
		self.game.screen.fill('black')
		self.game.screen.blit(self.bg, (480,115))
		for button in self.buttons:
			button.draw()

		self.particle1.emit()
		self.game.send_frame()
		self.accumulator += self.game.dt

class Options(Scene):
	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: HOME")
		self.bg = get_image("./assets/backgrounds/main-menu/KnK.png")
		self.buttons = [
			Button(self.game, "SOUND", (self.game.settings["screen_width"]//2, 320), Sound_Settings, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			Button(self.game, "FULLSCREEN", (self.game.settings["screen_width"]//2, 400), pg.display.toggle_fullscreen, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			Button(self.game, "CONTROLS", (self.game.settings["screen_width"]//2, 480), self.change_controls, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			Button(self.game, "BACK", (self.game.settings["screen_width"]//2, 560), Home_Screen, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			Button(self.game, "QUIT", (self.game.settings["screen_width"] - 100, 50), pg.quit, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
		]

		# mouse fx
		self.accumulator = 0
		self.particle1 = ParticlePrinciple()

	def change_controls(self):
		with open('settings.json', "r") as f:
			data = json.loads(f.read())
			
			#prompt for key
			print(data["controls"])
			key_to_change = input("what key do you wanna change: ")

			if key_to_change.upper() in data["controls"].keys():
				print('key found')
				for event in pg.event.get():
					if event.type == pg.KEYDOWN:
						data["controls"][key_to_change.upper()] = event.key
			else:
				print("key not found")
			#update settings json with new key

	def update(self):
		if self.accumulator >= 5 / 1000:
			mouse_pos = pg.mouse.get_pos()
			self.particle1.addParticles(mouse_pos[0], mouse_pos[1])
			self.accumulator = 0

		pressed_keys = pg.key.get_pressed()
		for event in pg.event.get():
			self.check_universal_events(pressed_keys, event)

			for button in self.buttons:
				button.update(event)

	def draw(self):
		self.game.screen.fill('black')
		self.game.screen.blit(self.bg, (480,115))
		for button in self.buttons:
			button.draw()

		self.particle1.emit()
		self.game.send_frame()
		self.accumulator += self.game.dt

class Local_Play(Scene):

	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(f"./assets/music/{SONGS[2]}.wav")
		pg.mixer.music.play(-1)

		self.game.player_1 = Fighter(game, 1, 200, 510, "Homusubi", "Play")
		self.game.player_2 = Fighter(game, 2, 1000, 570, "Homusubi", "Play")
		self.game.players = [self.game.player_2, self.game.player_1]  # reversed for client draw order

		COUNT_DOWN = pg.USEREVENT + 1
		self.game.match_time = 99
		self.game.time_accumulator = 0
		self.game.pressed_keys = pg.key.get_pressed()

	def update(self):
		if self.game.stun_frames >= self.game.max_stun_frames:
			self.game.hit_stun = False
		else:
			self.game.stun_frames += 0.5
		
		# process client events
		for event in pg.event.get():
			check_for_quit(event)

			if event.type == pg.KEYDOWN:
				if not self.game.hit_stun:
					self.game.player_1.handle_event(event)

					if event.key == pg.K_r:
						self.__init__(self.game)
						SceneManager(Main_Menu(self.game))

					if event.key == pg.K_h:
						pg.draw.rect(self.game.screen, "green", self.game.player_1.hit_box)

				if event.key == pg.K_ESCAPE:
					self.paused = True
					pause = Pause(self)
					pause.update()

		self.game.player_1.update(self.game.dt, self.game.player_2)
		self.game.player_2.update(self.game.dt, self.game.player_1)
		self.game.camera.update(self.game.player_1, self.game.player_2)


	def draw(self):
		# environment
		self.game.screen.fill('black')
		self.game.screen.blit(self.game.background.update(self.game.dt), (-self.game.camera.rect.x, -self.game.camera.rect.y))
		self.game.draw_HUD()
		self.game.show_fps()
		#if self.player_1.attack_rect is not None:
		#	pg.draw.rect(self.screen, "green", self.player_1.attack_rect)

		# srpites
		for player in self.game.players:
			player.draw()

		# damage text
		for player in self.game.players:
			if player.animated_text is not None:
				if player.animated_text.update():
					player.animated_text = None

		self.game.send_frame()
		self.game.time_accumulator += self.game.dt


class SceneManager:
	def __init__(self, start_scene):
		self.scene = start_scene
		
		
	def start(self):
		while True:
			self.scene.update()
			self.scene.draw()