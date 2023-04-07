import socket
import threading
import json

from scenes import LobbyView
from button import Button
from fighter import Event


class Client:
    def __init__(self, game, server_ip, server_port):
        self.game = game
        self.server_ip = server_ip
        self.server_port = server_port
        self.local_ip = self.get_ip()#local_ip
        self.local_port = 8001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.local_ip, self.local_port))
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listen_thread.start()
        self.session_list_callback = None  # set in lobby scene
        self.is_host = False 
        
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    # replaces the current server with a new one
    def set_server(self, client):
        ip, port = client
        self.server_ip = ip
        self.server_port = port

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.handle_message(data, addr)

    def handle_message(self, data, addr):
        try:
            decoded_data = json.loads(data.decode('utf-8'))
            if isinstance(decoded_data, int):
                return

            match decoded_data["type"]:
                # session list from lobby server
                case 'session_list':
                    if self.session_list_callback is not None:  # only update the session list if they are in the lobby menu
                        self.session_list_callback(decoded_data["sessions"])

                # a specific session's info from lobby server
                case 'session_info':
                    self.game.session = decoded_data["session"]

                # Host has initiated a handshake
                case 'handshake':
                    # set server to host client
                    self.set_server(self.game.session["clients"][0])
                    # finishes the hole-punch connection
                    self.send_message({"type": "ready"})  # at this point the server has been set to the Host
                    self.game.start_countdown = True

                # The clients have established a direct connection and are ready to start
                case 'ready':
                    self.game.start_countdown = True

                # events
                case 'event':
                    key = decoded_data["event"]
                    event = Event(key)
                    if self.is_host:  # recieved event from guest
                        self.game.player_2.handle_event(event)
                    else:  # recieved event from guest
                        self.game.player_1.handle_event(event)

                # pressed_keys
                case 'pressed_keys':
                    pressed_keys = {int(key): value for key, value in decoded_data["pressed_keys"].items()}
                    if self.is_host:  # recieved keys from guest
                        self.game.player_2.pressed_keys = pressed_keys
                    else:  # recieved keys from host
                        self.game.player_1.pressed_keys = pressed_keys

                # gamestate update
                case 'update':
                    p1_data = decoded_data["player_1"]
                    p2_data = decoded_data["player_2"]
                    self.game.player_1.from_dict(p1_data)
                    self.game.player_2.from_dict(p2_data)
                    self.game.match_time = decoded_data["match_time"]

                # host has left the session
                case 'disconnect':
                    self.game.sceneManager.scene = LobbyView(self.game)

        except Exception as e:
            print(f"Error while handling message from {addr}: {e}\n Data: {data}")

    def send_gamestate(self):
        p1 = self.game.player_1
        p2 = self.game.player_2
        gamestate = {
            "type": "update",
            "player_1": self.game.player_1.to_dict(),
            "player_2": self.game.player_2.to_dict(),
            "match_time": self.game.match_time
        }
        self.send_message(gamestate)

    def send_message(self, message, serialize=True, server=None):
        if server is None:
            server = (self.server_ip, self.server_port)
        try:
            if serialize:
                message = json.dumps(message).encode('utf-8')
            self.sock.sendto(message, server)
        except Exception as e:
            print(f"Error while sending message to ({server[0]}, {server[1]}): {e}\n Message: {message}")