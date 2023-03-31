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

"""
Refactor notes

All animations should use the same parent class and will have its own
frame_index variable, and the current time in ms since the last 
frame will be stored in game.dt

Each animation will have a speed parameter based on a dictionary containing
the values for each animation.

Fighter class will have an update method and a handle_event method. update
deals with non-input events like gravity, collision checks, etc.
handle_event is passed events from either the pygame event queue, the AI
action space, or the server data, but will all be handled the same way.

The handle_event method will also use self.combo and self.game.dt to determine
if any valid combinations of input have been made in a valid amount of time.
This method will also call an update to the current animation if there is one.

AI Mode
 - Player1 inputs from pygame event queue
 - Player2 inputs from AI model
 - 



"""

class Game:
	def __init__(self):
		settings.load()
		self.setup_pygame()
		self.import_assets()

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
		pg.mixer.music.load(self.settings["songs"]['main'])
		pg.mixer.music.play(-1)
		self.volume = self.settings["game_volume"]
		pg.mixer.music.set_volume(self.volume)

		# display
		self.screen = pg.display.set_mode((self.settings["screen_width"], self.settings["screen_height"]), )
		self.clock = pg.time.Clock()
		pg.display.set_icon(pg.image.load('./assets/icons/main/gameicon.ico'))
		pg.display.set_caption("Kami No Ken: GENESIS")
		self.background = Animator(game, self.bg_animations["ogre-gate"], ANIMATION_SPEEDS["bg"], loop=True)

	def import_assets(self):
		''' Load, scale, and store all primary assets in the game object '''

		# hud
		hud = get_image("./assets/ui/HUD/HUD.png")
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
		ratio = player.hp / FIGHTER_DATA[player.character]["max hp"]
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

		elif player.blast_cooldown > 0:
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

	def send_frame(self):
		self.dt = self.clock.tick(self.settings["FPS"]) / 1000
		pg.display.flip()

	def main_menu(self):
		pg.display.set_caption("Kami No Ken: MAIN MENU")
		bg = get_image("./assets/backgrounds/main-menu/KnK.png")
		bg_pos = bg.get_rect().center
		play_button = Button(self.settings["screen_width"]/2, self.settings["screen_height"]/2, 200, 100, "PLAY", self.HomeScreen)

		# mouse fx
		particle1 = ParticlePrinciple()
		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,5)

		while True:
			self.screen.fill('black')
			self.screen.blit(bg, bg_pos)

			for event in pg.event.get():
				check_for_quit(event)
				
				if event.type == PARTICLE_EVENT:
					mouse_pos = pg.mouse.get_pos()
					particle1.addParticles(mouse_pos[0], mouse_pos[1])

				play_button.Process(event)

			play_button.draw()
			particle1.emit()
			self.send_frame()

	def PlayLocal(self):
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(f"./assets/music/{SONGS['science']}")
		pg.mixer.music.play(-1)

		self.player_1 = Fighter(self, 200, 510, False, "Homusubi", self.dt)
		self.player_2 = Fighter(self, 1000, 570, True, "Homusubi", self.dt)
		self.players = [self.player_2, self.player_1]  # reversed for client draw order

		COUNT_DOWN = pg.USEREVENT + 1
		self.match_time = 99
		self.match_time_text = "99"

		while True:

			self.screen.fill('grey')
			self.animate()
			self.drawBG()

			for player in self.players:
				first_player = player == self.player_1

				if first_player:
					other_player = self.player_2
				else:
					other_player = self.player_1

				#update fighters
				if not self.hit_stun:
					player.move(other_player)
					player.updateAnim(other_player)

					player.framesWithoutCombo += 1
					if player.framesWithoutCombo > 26 or len(player.moveCombo) > 9:
						player.framesWithoutCombo = 0
						player.moveCombo = []
				else:
					if self.stun_frames >= self.max_stun_frames:
						self.hit_stun = False
					else:
						self.stun_frames += 0.5  # add by half for each player

				# process p1 events
				if first_player:
					for event in pg.event.get():
						check_for_quit(event)

						if event.type == COUNT_DOWN:
							dt = self.dt
							self.match_time -= dt
							self.match_time_text = str(int(self.match_time)) if int(self.match_time) > 0 else '00'
							if int(self.match_time) == 0:
								self.match_time = 0
								print("match over")

						if event.type == pg.KEYDOWN:
							if not self.hit_stun:
								self.player_1.handle_keydowns(event, self.player_2)
								self.player_1.moveCombo.append(event.key)
								# self.player_2.moveCombo.append(event.key)

								if event.key == pg.K_r:
									self.__init__()
									self.MainMenu()

								if event.key == pg.K_h:
									pg.draw.rect(self.screen, "green", self.player_1.hit_box)
							
							if event.key == pg.K_ESCAPE:
								self.paused = True
								pause = Pause(self)
								pause.update()

							
				# draw player
				player.draw()

			#show player stats
			self.draw_HUD()
			self.draw_portrait(self.player_1)
			self.draw_portrait(self.player_2)

			for player in self.players:
				if player.animated_text is not None:
					if player.animated_text.update():
						player.animated_text = None

			# match clock
			draw_text(self.screen, self.match_time_text[:-1], (self.settings["screen_width"]/2 - 50, 80), 120, (255, 0, 0))
			draw_text(self.screen, self.match_time_text[-1:], (self.settings["screen_width"]/2 + 50, 80), 120, (255, 0, 0))

			# show self.settings["fps"]
			fpsCounter = round(self.clock.get_fps())
			draw_text(self.screen, f"FPS: {fpsCounter}", (self.settings["screen_width"]/2, 200))

			self.send_frame()