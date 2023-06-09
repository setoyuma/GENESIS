import pygame as pg
import threading
import json
import time
import sys

from color_animation import ColorGradient
from particle import ParticlePrinciple
from fighter import Fighter, Event
from animation import Animator
from client import Client
from camera import Camera
from button import Button
from slider import Slider
from pause import Pause
from show_inputs import *
from constants import * 
from support import *
from scenes import *

health_bar_colors = ColorGradient((0,255,0), (255,0,0)).generate_gradient()
blast_polygon_colors = ColorGradient((255,255,255), (255,255,0)).generate_gradient()

# br ~ tr ~ tl ~ bl  br=0                          # tr=3     # tl=4               # bl=6
blast_points = [(179, 127), (195, 99), (225, 98), (225, 95), (30, 85), (6, 113), (28, 137), (53, 123), (92, 112), (173, 127)]
right_blast_points = [(1421, 127), (1405, 99), (1375, 98), (1375, 95), (1570, 85), (1594, 113), (1572, 137), (1547, 123), (1508, 112), (1427, 127)]


class Game:
	def __init__(self):
		pg.init()
		pg.key.set_repeat(0)
		self.load_settings()
		self.screen = pg.display.set_mode((self.settings["screen_width"], self.settings["screen_height"]), pg.SCALED)
		self.import_assets()
		self.setup_pygame()

		self.client = Client(self, "45.56.77.161", 8001)  # client sends data to lobby server by default
		self.heartbeat_thread = threading.Thread(target=self.send_heartbeat, args=(self.client,), daemon=True)  # Use a separate thread to send a heartbeat
		self.heartbeat_thread.start()

		# Game BG + BG Animation
		# Instantiate the camera with the size of the window
		self.camera = Camera(self.settings["screen_width"], self.settings["screen_height"])
		self.frame_index = 0
		self.animation_speed = 0.25
		self.hit_stun = False
		self.stun_time = 0
		self.max_stun_time = 0

	def send_heartbeat(self, client):
		while True:  # Send a heartbeat every 3 seconds
			time.sleep(3)
			data = {"type": "heartbeat"}
			self.client.send_message(data, server=("45.56.77.161", 8001))

	def load_settings(self):
		with open('settings.json', 'r') as f:
			self.settings = json.loads(f.read())

		# Resolution
		self.HALF_SCREENW = self.settings["screen_width"] // 2
		self.HALF_SCREENH = self.settings["screen_height"] // 2
		self.QUARTER_SCREENW = self.settings["screen_width"] // 4
		self.QUARTER_SCREENH = self.settings["screen_width"] // 4

	def setup_pygame(self):
		# music and sound
		pg.mixer.init()
		pg.mixer.music.load(f"./assets/music/{SONGS[0]}.wav")
		pg.mixer.music.play(-1)
		self.volume = self.settings["game_volume"]
		pg.mixer.music.set_volume(self.volume)
		self.bg = BACKGROUNDS["carnival"]
		self.animation = Animator(self, self.bg, 0.25)

		# display
		self.clock = pg.time.Clock()
		pg.display.set_icon(pg.image.load('./assets/icons/main/gameicon.ico'))
		pg.display.set_caption("Kami No Ken: GENESIS")
		self.background = Animator(self, self.bg_animations[self.bg], FRAME_DURATIONS["bg"], loop=True)

	def import_assets(self):
		''' Load, scale, and store all primary assets in the game object '''

		# hud
		hud = get_image("./assets/ui/HUD/HUD4.png")
		self.hud = pg.transform.scale(hud, (self.settings["screen_width"],  self.settings["screen_height"]/3))
		self.hud_bg_surf = pg.Surface((self.settings["screen_width"], self.settings["screen_height"]/2), pygame.SRCALPHA)
		self.particle1 = ParticlePrinciple()

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
			self.super_meter_sparks(player)
		
	def super_meter_sparks(self, player):
		if player.super_meter >= 250:
			start_angle, end_angle = 280, 430
			x = 610
			color = "red"
			if player.AI:
				start_angle += 180
				end_angle += 180
				x += 390
				color = "blue"
			self.particle1.addParticles(x, 138, color, start_angle, end_angle, 8)
			self.particle1.emit()

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
		
		color = health_bar_colors[color_index]
		if player.hit:
			color = (255,255,255)

		match player:
			case self.player_1:
				pg.draw.polygon(self.screen, color, [(30+(600*ratio), 85+(ratio*27)), (30+(600*ratio), 67-(ratio*27)), (30, 65), (30, 85)])
			case self.player_2:
				pg.draw.polygon(self.screen, color, [(right_x-(600*ratio), 85+(ratio*27)), (right_x-(600*ratio), 67-(ratio*27)), (right_x, 65), (right_x, 85)])

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

	def handle_event(self, event):
		if self.client.is_host:
			self.player_1.handle_event(event)
		else:
			self.player_2.handle_event(event)
		# send event to the other client
		self.client.send_message({"type": "event", "event": event.key})

	def start_match(self):
		if not len(self.session["clients"]) == 2:
			print("2 players required to start a match.")
			return
		# send a packet to Guest
		guest_client = self.session["clients"][1]
		self.client.sock.sendto(b'0', (guest_client[0], guest_client[1]))
		# tell Lobby you started a handshake
		self.client.send_message({"type": "handshake"})
		# host no longer needs to interact with lobby (assuming hole-punch goes well)
		self.client.set_server(guest_client)

	def end_match(self):
		pass


if __name__ == '__main__':
	game = Game()
	game.sceneManager = SceneManager(Main_Menu(game))
	game.sceneManager.start()