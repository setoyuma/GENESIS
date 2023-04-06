import pygame as pg
import json

from particle import ParticlePrinciple
from fighter import Fighter
from button import Button
from slider import Slider
from pause import Pause
from show_inputs import *
from constants import *
from support import *


class Scene:
    def __init__(self, game, initial_bg=None):
        self.game = game
        self.active = True
        self.obscured = False

    def update(self):
        pass

    def draw(self):
        pass

    def check_universal_events(self, pressed_keys, event):
        quit_attempt = False
        if event.type == pygame.QUIT:
            quit_attempt = True
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or \
                            pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True
        if quit_attempt:
            pygame.quit()
            sys.exit()


class Match(Scene):
	def __init__(self, game):
		super().__init__(game)

	def draw_stage(self):
		self.game.screen.fill('black')
		self.game.screen.blit(self.game.background.update(self.game.dt), (-self.game.camera.rect.x, -self.game.camera.rect.y))
		self.game.draw_HUD()
		self.game.show_fps()
		#if self.player_1.attack_rect is not None:
		#	pg.draw.rect(self.screen, "green", self.player_1.attack_rect)

	def draw_players(self):
		# srpites
		for player in self.game.players:
			player.draw()

		# damage text
		for player in self.game.players:
			if player.animated_text is not None:
				if player.animated_text.update():
					player.animated_text = None

	def update_hit_stun(self):
		if self.game.stun_frames >= self.game.max_stun_frames:
			self.game.hit_stun = False
		else:
			self.game.stun_frames += 0.5

	def check_pause(self, event):
		if event.key == pg.K_ESCAPE:
			self.game.paused = True
			pause = Pause(self.game)


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


class Home_Screen(Scene):
	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: HOME")
		self.bg = get_image("./assets/backgrounds/main-menu/KnK.png")
		self.buttons = [
			Button(game, "LOCAL",(70,40), Local_Play,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			Button(game, "ONLINE",(70,120), LobbyView,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			Button(game, "BACK",(70,200), Main_Menu,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			Button(game, "OPTIONS",(70,280), Options,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			Button(game, "TRAINING",(70,360), Training,"assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png"),
			Button(game, "QUIT", (self.game.settings["screen_width"]-100,50), pg.quit, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png")
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


class Local_Play(Match):
	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(f"./assets/music/{SONGS[2]}.wav")
		pg.mixer.music.play(-1)

		self.game.player_1 = Fighter(game, 1, 200, 510, "Homusubi", "Play")
		self.game.player_2 = Fighter(game, 2, 1000, 510, "Homusubi", "Play")
		self.game.player_2.pressed_keys = {119: False, 115: False, 97: False, 100: False, 1073742050: False, 1073742054: False, 1073741885: False}
		self.game.players = [self.game.player_2, self.game.player_1]  # reversed for client draw order
		self.game.match_time = 99
		self.game.time_accumulator = 0

	def update(self):
		self.game.player_1.pressed_keys = pg.key.get_pressed()
		# process client events
		for event in pg.event.get():
			self.check_universal_events(self.game.player_1.pressed_keys, event)

			if event.type == pg.KEYDOWN:
				self.check_pause(event)
				if not self.game.hit_stun:
					self.game.player_1.handle_event(event)

					if event.key == pg.K_r:
						self.__init__(self.game)
						SceneManager(Main_Menu(self.game))

					if event.key == pg.K_h:
						pg.draw.rect(self.game.screen, "green", self.game.player_1.hit_box)

		self.update_hit_stun()
		self.game.player_1.update(self.game.dt, self.game.player_2)
		self.game.player_2.update(self.game.dt, self.game.player_1)
		self.game.camera.update(self.game.player_1, self.game.player_2)

	def draw(self):
		self.draw_stage()
		self.draw_players()
		self.game.send_frame()
		self.game.time_accumulator += self.game.dt


class Training(Match):
	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: TRAINING")
		pg.mixer.music.load(f"./assets/music/{SONGS[2]}.wav")
		pg.mixer.music.play(-1)

		self.game.player_1 = Fighter(self.game, 1, 200, 510, "Homusubi", "Play")
		self.game.player_2 = Fighter(self.game, 2, 1000, 570, "Homusubi", "Play")
		self.game.player_2.pressed_keys = {119: False, 115: False, 97: False, 100: False, 1073742050: False, 1073742054: False, 1073741885: False}
		self.game.players = [self.game.player_2, self.game.player_1]  # reversed for client draw order
		self.user_buttons = User_Inputs(self.game.settings["screen_width"]//2, 200, 30, self.game.player_1)
		self.game.time_accumulator = 0
		self.game.match_time = 99

	def update(self):
		self.game.player_1.pressed_keys = pg.key.get_pressed()
		# process client events
		for event in pg.event.get():
			self.check_universal_events(self.game.player_1.pressed_keys, event)

			if event.type == pg.KEYDOWN:
				self.check_pause(event)
				if not self.game.hit_stun:
					self.game.player_1.handle_event(event)

					if event.key == pg.K_r:
						self.game.__init__()
						SceneManager(Main_Menu(self.game))

					if event.key == pg.K_h:
						pg.draw.rect(self.game.screen, "green", self.game.player_1.hit_box)

		self.update_hit_stun()
		self.game.player_1.update(self.game.dt, self.game.player_2)
		self.game.player_2.update(self.game.dt, self.game.player_1)
		self.game.camera.update(self.game.player_1, self.game.player_2)

	def draw(self):
		self.draw_stage()
		self.user_buttons.draw()
		self.draw_players()
		self.game.send_frame()
		self.game.time_accumulator += self.game.dt


class LobbyView(Scene):
	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: LOBBY PLAY")
		self.mainMenuBG = get_image("./assets/backgrounds/main-menu/KnK.png")
		self.particle1 = ParticlePrinciple()
		self.accumulator = 0
		self.buttons = [
			Button(self.game, "CREATE", (self.game.settings["screen_width"]/3+960, 700), self.create_session, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			Button(self.game, "BACK", (self.game.settings["screen_width"]//3+760, 700), Home_Screen, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30)
		]
		self.game.client.session_list_callback = self.populate_session_list
		self.game.session_buttons = []
		self.game.session = None
		self.get_session_list()
		self.game.start_countdown = False

	def update(self):
		if self.game.start_countdown:
			self.game.sceneManager.scene = Online_play(self.game)

		if self.accumulator >= 5 / 1000:
			mouse_pos = pg.mouse.get_pos()
			self.particle1.addParticles(mouse_pos[0], mouse_pos[1])
			self.accumulator = 0

		pressed_keys = pg.key.get_pressed()
		for event in pg.event.get():
			self.check_universal_events(pressed_keys, event)

			for button in self.buttons:
				button.update(event)
			for session_button in self.game.session_buttons:
				session_button.update(event)

	def draw(self):
		self.game.screen.fill('black')
		self.game.screen.blit(self.mainMenuBG,(480,115))

		# session view
		pg.draw.rect(self.game.screen, (200,100,0), (1250, 150, 300, 500), width=2, border_radius=1)
		if self.game.session is None:
			# list sessions to join
			draw_text(self.game.screen, "Online sessions", (1400, 115), 40)
			for session_button in self.game.session_buttons:
				session_button.draw()
		else:
			# draw the session information
			draw_text(self.game.screen, self.game.session["name"], (1400, 100), 40)
			for i in range(len(self.game.session["clients"])):
				draw_text(self.game.screen, f"Player {i+1}", (1320, 175+(i*40)))

		for button in self.buttons:
			button.draw()
		
		self.particle1.emit()
		self.game.send_frame()
		self.accumulator += self.game.dt

	def populate_session_list(self, sessions):
		self.game.session_buttons = []
		for i, session in enumerate(sessions):
			button = Button(self.game, session["name"], (1400, 45*i+175), self.join_session, (0,0,290,40), (0,0,290,40), (0,0,200,150), (0,0,250,200), text_size=26, id=session["id"])
			self.game.session_buttons.append(button)

	def get_session_list(self):
		# refresh the session list
		data = {"type" : 'list_sessions'}
		self.game.client.send_message(data)

	def create_session(self):
		# turn client into host
		self.game.client.is_host = True
		self.game.session = {
			"name": "Test session",
			"clients": [self.game.client.local_ip],  # will be overwritten but needed
			"joinable": True,
			"id": None
		}

		# send a registration request to the lobby server
		data = {
			"type": "register_session",
			"session_info": self.game.session
		}
		self.game.client.send_message(data)

		# reinitialize buttons list with leave option
		self.buttons = [
			Button(self.game, "Start", (self.game.settings["screen_width"]/3+960, 700), self.game.start_match, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			Button(self.game, "Leave", (self.game.settings["screen_width"]/3+760, 700), self.leave_session, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
		]

	def join_session(self, id):
		# request a session's info from lobby server
		data = {
			"type": "join_session",
			"id": id
		}
		self.game.client.send_message(data)
		self.buttons = [Button(self.game, "Leave", (self.game.screen.get_width()/2+605, 700), self.leave_session, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30, id=None)]

	def leave_session(self):
		data = {
			"id": self.game.session["id"]
		}
		if self.game.client.is_host:
			# delete the session
			data["type"] = "unregister_session"
		else:
			# leave the session
			data["type"] = "disconnect"
		self.game.client.send_message(data)
		self.game.session = None
		self.buttons = [
			Button(self.game, "CREATE", (self.game.settings["screen_width"]/3+960, 700), self.create_session, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30),
			Button(self.game, "BACK", (self.game.settings["screen_width"]//3+760, 700), Home_Screen, "assets/ui/buttons/button_plate1.png", "assets/ui/buttons/button_plate1.png", text_size=30)
		]
		self.get_session_list()


class Online_play(Match):
	def __init__(self, game):
		super().__init__(game)
		pg.display.set_caption("Kami No Ken: GENESIS")
		pg.mixer.music.load(f"./assets/music/{SONGS[2]}.wav")
		pg.mixer.music.play(-1)

		self.game.player_1 = Fighter(self.game, 1, 200, 510, "Homusubi", "Play")
		self.game.player_2 = Fighter(self.game, 2, 1000, 510, "Homusubi", "Play")
		self.game.players = [self.game.player_2, self.game.player_1]  # reversed for client draw order
		self.game.player_1.pressed_keys = {119: False, 115: False, 97: False, 100: False, 1073742050: False, 1073742054: False, 1073741885: False}
		self.game.player_2.pressed_keys = {119: False, 115: False, 97: False, 100: False, 1073742050: False, 1073742054: False, 1073741885: False}
		self.game.gamestate_buffer = []
		self.game.match_started = False
		self.game.time_accumulator = 0
		self.game.match_time = 99
		self.fixed_time_step = 1.0 / self.game.settings["FPS"]  # Fixed time step in seconds for updating and sending inputs
		self.timestep_accumulator = 0
		self.countdown = 5.0
		self.prematch()

	# pre-match
	def prematch(self):
		while self.countdown > 0.0:
			self.draw_stage()
			self.draw_players()
			draw_text(self.game.screen, str(int(self.countdown)), (self.game.HALF_SCREENW, self.game.HALF_SCREENH))
			self.game.send_frame()
			self.countdown -= self.game.dt

	# match
	def update(self):
		self.game.time_accumulator += self.game.dt
		self.timestep_accumulator += self.game.dt

		pressed_keys = pg.key.get_pressed()
		self.send_pressed_keys(pressed_keys)

		if self.game.client.is_host:
			self.game.player_1.pressed_keys = pressed_keys
		else:
			self.game.player_2.pressed_keys = pressed_keys

		for event in pg.event.get():
			self.check_universal_events(pressed_keys, event)

			if event.type == pg.KEYDOWN:
				if not self.game.hit_stun:
					self.game.handle_event(event)

				if event.key == pg.K_ESCAPE:
					pass  # create confirmation dialog for leaving the match

		# do as many gamestate updates as necessary to catch up
		while self.timestep_accumulator >= self.fixed_time_step:
			self.timestep_accumulator -= self.fixed_time_step
			self.update_hit_stun()
			self.game.player_1.update(self.fixed_time_step, self.game.player_2)
			self.game.player_2.update(self.fixed_time_step, self.game.player_1)

	def draw(self):
		self.draw_stage()
		self.draw_players()
		self.game.send_frame()

	def send_pressed_keys(self, pressed_keys):
		pk_data = {119: False, 115: False, 97: False, 100: False}
		pk_data[Actions.UP] = pressed_keys[Actions.UP]
		pk_data[Actions.DOWN] = pressed_keys[Actions.DOWN]
		pk_data[Actions.BACK] = pressed_keys[Actions.BACK]
		pk_data[Actions.FORWARD] = pressed_keys[Actions.FORWARD]
		self.game.client.send_message({"type": "pressed_keys","pressed_keys": pk_data})


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


class SceneManager:
	def __init__(self, start_scene):
		self.scene = start_scene

	def start(self):
		while True:
			scene = self.scene
			self.scene.update()
			if scene != self.scene:  # scene has changed
				continue
			self.scene.draw()