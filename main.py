import pygame as pg
import sys
import json

from fighter import Fighter
from particle import ParticlePrinciple
from color_animation import ColorGradient
from animation import Animator
from button import Button
from slider import Slider
from pause import Pause
from constants import * 
from support import *

health_bar_colors = ColorGradient((0,255,0), (255,0,0)).generate_gradient()
blast_polygon_colors = ColorGradient((255,255,255), (255,255,0)).generate_gradient()

# br ~ tr ~ tl ~ bl  br=0                          # tr=3     # tl=4               # bl=6
blast_points = [(179, 127), (195, 99), (225, 98), (225, 95), (30, 85), (6, 113), (28, 137), (53, 123), (92, 112), (173, 127)]
right_blast_points = [(1421, 127), (1405, 99), (1375, 98), (1375, 95), (1570, 85), (1594, 113), (1572, 137), (1547, 123), (1508, 112), (1427, 127)]

class Game:
	def __init__(self):
		self.load_settings()
		self.import_assets()
		self.setup_pygame()

		self.hit_stun = None	

		# Game BG + BG Animation
		self.bg = BACKGROUNDS["carnival"]
		self.animation = Animator(self, self.bg, 0.25)
		self.frame_index = 0
		self.animation_speed = 0.25
		self.stun_frames = 0
		self.max_stun_frames = 0

	def load_settings(self):
		with open('settings.json', 'r') as f:
			self.settings = json.loads(f.read())

		# Resolution
		self.HALF_SCREENW = self.settings["screen_width"] // 2
		self.HALF_SCREENH = self.settings["screen_height"] // 2
		self.QUARTER_SCREENW = self.settings["screen_width"] // 4
		self.QUARTER_SCREENH = self.settings["screen_width"] // 4

	def setup_pygame(self):
		pg.init()

		# music and sound
		pg.mixer.init()
		pg.mixer.music.load(f"./assets/music/{SONGS[0]}.wav")
		pg.mixer.music.play(-1)
		self.volume = self.settings["game_volume"]
		pg.mixer.music.set_volume(self.volume)

		# display
		self.screen = pg.display.set_mode((self.settings["screen_width"], self.settings["screen_height"]), pg.SCALED)
		self.clock = pg.time.Clock()
		pg.display.set_icon(pg.image.load('./assets/icons/main/gameicon.ico'))
		pg.display.set_caption("Kami No Ken: GENESIS")
		self.background = Animator(self, self.bg_animations["ogre-gate"], FRAME_DURATIONS["bg"], loop=True)

	def import_assets(self):
		''' Load, scale, and store all primary assets in the game object '''

		# hud
		hud = get_image("./assets/ui/HUD/HUD4.png")
		self.hud = pg.transform.scale(hud, (self.settings["screen_width"],  self.settings["screen_height"]/3))
		self.hud_bg_surf = pg.Surface((self.settings["screen_width"], self.settings["screen_height"]/2), pygame.SRCALPHA)

		# portaits
		size = 80
		self.portraits = {}
		for character in FIGHTER_DATA.keys():
			portrait = get_image(f"./assets/characters/{character}/portrait/portrait.png")
			portrait = pg.transform.scale(portrait, (size+20, size-10))
			self.portraits[character] = portrait

		# background
		self.bg_animations = {"bay-side-carnival": [], "ogre-gate": []}
		for animation in self.bg_animations.keys():
			full_path = f'./assets/backgrounds/{animation}'
			original_images = import_folder(full_path)
			scaled_images = scale_images(original_images, (self.settings["screen_width"], self.settings["screen_height"]))
			self.bg_animations[animation] = scaled_images

	def draw_HUD(self):
		self.draw_hud_bg()
		for player in self.players:
			self.drawHealthBar(player)
			self.draw_super_meter(player)
			self.draw_blast_meter(player)
			self.screen.blit(self.hud, (0,-55))
			self.draw_portrait(player)
			self.show_match_time()
	
	def draw_hud_bg(self):
		bg_color = (40,40,40,200)
		self.hud_bg_surf.fill((0,0,0,0))
		screen_width = self.settings["screen_width"]
		right_x = screen_width - 33

		# p1 hp
		pg.draw.polygon(self.hud_bg_surf, bg_color, [(30+(600*1), 85+(1*27)), (30+(600*1), 67-(1*27)), (30, 65), (30, 85)])
		# p1 super
		pg.draw.polygon(self.hud_bg_surf, bg_color, [(190 + (1 * 635), 113 + (1 * 54)), (200 + (1 * 615), 93 + (1 * 26)), (200 , 93), (190, 113)])
		# p2 hp
		pg.draw.polygon(self.hud_bg_surf, bg_color, [(right_x-(600*1), 85+(1*27)), (right_x-(600*1), 67-(1*27)), (right_x, 65), (right_x, 85)])
		# p2 super
		pg.draw.polygon(self.hud_bg_surf, bg_color, [(screen_width - (190 + (1 * 635)), 113 + (1 * 54)), (screen_width - (200 + (1 * 615)), 93 + (1 * 26)), (screen_width - 200 , 93), (screen_width - 190, 113)])
		
		self.screen.blit(self.hud_bg_surf, (0,0))

	def drawHealthBar(self, player):
		ratio = player.current_hp / FIGHTER_DATA[player.character]["max hp"]
		screen_width = self.settings["screen_width"]
		right_x = screen_width - 33

		# determines color in the gradient list
		color_index = len(health_bar_colors) - int(ratio * len(health_bar_colors))
		if color_index >= len(health_bar_colors):
			color_index = len(health_bar_colors) - 1

		match player:
			case self.player_1:
				pg.draw.polygon(self.screen, health_bar_colors[color_index], [(30+(600*ratio), 85+(ratio*27)), (30+(600*ratio), 67-(ratio*27)), (30, 65), (30, 85)])
			case self.player_2:
				pg.draw.polygon(self.screen, health_bar_colors[color_index], [(right_x-(600*ratio), 85+(ratio*27)), (right_x-(600*ratio), 67-(ratio*27)), (right_x, 65), (right_x, 85)])

	def draw_super_meter(self, player):
		screen_width = self.settings["screen_width"]
		super_meter_ratio = (player.super_meter / 250) * .68

		match player:
			case self.player_1:
				pg.draw.polygon(self.screen, "red", [(190 + (super_meter_ratio * 635), 113 + (super_meter_ratio * 54)), (200 + (super_meter_ratio * 615), 93 + (super_meter_ratio * 26)), (200 , 93), (190, 113)])
			case self.player_2:
				pg.draw.polygon(self.screen, "blue", [(screen_width - (190 + (super_meter_ratio * 635)), 113 + (super_meter_ratio * 54)), (screen_width - (200 + (super_meter_ratio * 615)), 93 + (super_meter_ratio * 26)), (screen_width - 200 , 93), (screen_width - 190, 113)])

	def draw_blast_meter(self, player):
		match player:
			case self.player_1:
				points = blast_points
			case self.player_2:
				points = right_blast_points

		if player.super_meter >= 50 and player.blast_cooldown == 0:
			if player.blast_meter < len(blast_polygon_colors)-2:
				player.blast_meter += 2
		else:
			player.blast_meter = 0

		pg.draw.polygon(self.screen, blast_polygon_colors[player.blast_meter], points)

	def draw_portrait(self, player):
		portrait = self.portraits[player.character]

		match player:
			case self.player_1:
				pos = (50, 2)
			case self.player_2:
				pos = (1460, 2)
			
		portrait = pg.transform.flip(portrait, True, False)
		self.screen.blit(portrait, pos)

	def show_match_time(self):
		if self.time_accumulator >= 1:
			self.match_time -= 1
			self.time_accumulator -= 1

			if self.match_time <= 0:
				self.match_time = 0
				self.end_match()

		time = str(self.match_time)
		for i, char in enumerate(time):
			draw_text(self.screen, char, ((self.settings["screen_width"]/2 - 50) + (i*100), 80), 120, (255,0,0))

	def show_fps(self):
		fpsCounter = round(self.clock.get_fps())
		draw_text(self.screen, f"FPS: {fpsCounter}", (self.settings["screen_width"]/2, 200))

	def send_frame(self):
		self.dt = self.clock.tick(self.settings["FPS"]) / 1000.0
		pg.display.flip()

	def main_menu(self):
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		bg = get_image("./assets/backgrounds/main-menu/KnK.png")
		bg_pos = bg.get_rect().center # wouldnt line up in center for some reason
		buttons = [
			Button(self.settings["screen_width"]/2, self.settings["screen_height"]/2, 200, 100, 30, "PLAY", self.home_screen),
			Button(self.settings["screen_width"] - 100, 0 - 10, 200, 100, 30, "QUIT", pg.quit),
		]

		# mouse fx
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)

		while True:
			self.screen.fill('black')
			self.screen.blit(bg, (480,115))

			for event in pg.event.get():
				check_for_quit(event)
				
				if event.type == PARTICLE_EVENT:
					mouse_pos = pg.mouse.get_pos()
					particle1.addParticles(mouse_pos[0], mouse_pos[1])

				for button in buttons:
					button.Process(event)
			
			for button in buttons:
				button.draw()
			
			particle1.emit()
			self.send_frame()

	def home_screen(self):
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)
		buttons = [
			Button(70, 40, 200, 100, 30, "LOCAL", self.play_local),
			Button(70, 200, 200, 100, 30, "BACK", self.main_menu),
			#Button(70, 120, 200, 100, 30, "TRAINING", self.training),
			Button(70, 280, 200, 100, 30, "OPTIONS", self.options),
			Button(self.settings["screen_width"] - 100, 0 - 10, 200, 100, 30, "QUIT", pg.quit),
		]
		while True:
			self.screen.fill('black')
			self.screen.blit(mainMenuBG,(480,115))

			for event in pg.event.get():
				check_for_quit(event)
	
				if event.type == PARTICLE_EVENT:
					mouse_pos = pg.mouse.get_pos()
					particle1.addParticles(mouse_pos[0], mouse_pos[1])
            
				for button in buttons:
					button.Process(event)

			for button in buttons:
				button.draw()

			particle1.emit()
			self.send_frame()

	def options(self):
		pg.display.set_caption("Kami No Ken: OPTIONS")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)
		buttons = [
			Button(self.settings["screen_width"]//2, 480, 200, 100, 30, "BACK", self.home_screen),
			Button(self.settings["screen_width"]//2, 320, 200, 100, 30, "SOUND", self.sound_settings),
			Button(self.settings["screen_width"]//2, 400, 200, 100, 30, "FULLSCREEN", pg.display.toggle_fullscreen),
			Button(self.settings["screen_width"] - 100, 0 - 10, 200, 100, 30, "QUIT", pg.quit),
		]
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
            
				for button in buttons:
					button.Process(event)

			for button in buttons:
				button.draw()

			particle1.emit()
			self.send_frame()

	def sound_settings(self):
		pg.display.set_caption("Kami No Ken: SOUND SETTINGS")
		mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)
		slider = Slider(self.settings["screen_width"]/2 - 95, 145, 200, 10, self.volume)
		volume_button = Button(self.settings["screen_width"]/2, 40, 200, 100, 30, "VOLUME", None)
		back_button = Button(self.settings["screen_width"]/2, 160, 200, 100, 30,"BACK", self.options)
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

	def play_local(self):
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(f"./assets/music/{SONGS[2]}.wav")
		pg.mixer.music.play(-1)

		self.player_1 = Fighter(self, 1, 200, 510, "Homusubi", "Play")
		self.player_2 = Fighter(self, 2, 1000, 570, "Homusubi", "Play")
		self.players = [self.player_2, self.player_1]  # reversed for client draw order

		COUNT_DOWN = pg.USEREVENT + 1
		self.match_time = 99
		self.time_accumulator = 0

		while True:
			if self.stun_frames >= self.max_stun_frames:
				self.hit_stun = False
			else:
				self.stun_frames += 0.5

			# process client events
			for event in pg.event.get():
				check_for_quit(event)

				if event.type == pg.KEYDOWN:
					if not self.hit_stun:
						self.player_1.handle_event(event)

						if event.key == pg.K_r:
							self.__init__()
							self.main_menu()

						if event.key == pg.K_h:
							pg.draw.rect(self.screen, "green", self.player_1.hit_box)

					if event.key == pg.K_ESCAPE:
						self.paused = True
						pause = Pause(self)
						pause.update()
			
			self.player_1.update(self.dt, self.player_2)
			self.player_2.update(self.dt, self.player_1)

			# environment
			self.screen.fill('black')
			self.screen.blit(self.background.update(self.dt), (0,0))
			self.draw_HUD()
			self.show_fps()
			#if self.player_1.attack_rect is not None:
			#	pg.draw.rect(self.screen, "green", self.player_1.attack_rect)

			# srpites
			for player in self.players:
				player.draw()

			# damage text
			for player in self.players:
				if player.animated_text is not None:
					if player.animated_text.update():
						player.animated_text = None

			self.send_frame()
			self.time_accumulator += self.dt

	def end_match(self):
		pass

if __name__ == '__main__':
	game = Game()
	game.main_menu()