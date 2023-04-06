import socket
import threading
import json

from button import Button
from fighter import Event

"""
NETCODE DOCS

An instance of Client is created when the user
goes into the online menu. The client initially
connects to the central lobby server and
requests the session list.

If the user chooses to create a session, their
client will be marked as a host and a session will
be initiated on the lobby server. The user will 
then have the option of leaving the session, or
starting the match once another player connects.

When the match is started, the clients exchange info
with each other through the lobby server to initiate 
a direct connection using hole-punching before loading 
into the online_play scene.

The host is player_1 and the guest is player_2. Once 
the guest sends the host a 'ready' message, a 
countdown begins and the match starts.

The host processes its own events as well as the 
guest's events. The host sends a gamestate update 
to the guest every frame.

1. Player starts the game
2. Game creates an instance of Client
3. Player clicks 'create session'
4. The host sends a message to the lobby server asking for session registration
5. The player's client is marked as the session host
6. Another client decides to join the session
7. Host starts the match
8. The clients exchange information with each other through the lobby server using STUN
9a. The clients initiate a direct connection with each other
9b (OPTIONAL) If a direct connection is not possible, use the lobby server as a relay
10a. The player 2 client sends events to the host
10b. The player 1 client manages the gamestate and sends it to player 2

NAT HOLE-PUNCHING
------------------
Normally, to receive messages from the internet, a client needs to forward a port on their router, which directs 
incoming packets to the correct computer on the network. Hole-punching is a technique that establishes a direct 
connection between two clients without port forwarding.

1. Clients exchange their public IPs and ports via a lobby server.
2. Client_1 sends an initial packet to Client_2's public IP. Although this packet doesn't reach Client_2 due to the lack of port forwarding, Client_1's router now associates Client_1's private IP with Client_2's public IP.
3. Client_2 sends a response packet to Client_1. Thanks to the previous association, this packet reaches Client_1, and a similar association is created on Client_2's router.
4. As long as messages are sent periodically to maintain the associations on both clients' routers, the connection is maintained.

This is our implementation of hole-punching:

1. Host sends a 'start_match' message to the Lobby.
2. Lobby sends a 'client_info' message to both clients, containing each other's IPs and ports.
3. Host sends an initial packet to Guest (doesn't reach Guest but creates a mapping between Host and Guest on Host's router).
4. Host sends a 'handshake' message to the Lobby (indicating the first part of the handshake is complete).
5. Lobby forwards the 'handshake' message to Guest (informing Guest that Host initiated a handshake and requires a response).
6. Guest sends a response packet to Host, completing the hole-punch (creates a mapping between Guest and Host on Guest's router).
7. A direct connection is established, and Host begins the match start countdown.

STUN and TURN
--------------
A STUN server is an intermediary server that helps clients exchange their public IPs and ports, enabling them to 
establish a hole-punch connection. In this game, the lobby server will function as the STUN server.

A TURN server is another type of intermediary server or relay that clients can use for communication when 
hole-punching fails. If necessary, the lobby server can also act as a TURN server.

ICE
----
ICE (Interactive Connectivity Establishment) is a framework that combines the above techniques (STUN and TURN) 
along with other fallback protocols. While these more complex protocols may not be necessary for this game, ICE 
ensures that the best possible connection method is used for communication between clients.


Gamestate synchronization
---------------------------
Setting up the main loop:
 - scenes need to be turned into classes (easy) so they can have a separate update and draw method because update may be called multiple times a frame
 - both clients will store a buffer of gamestates and send their events in fixed timesteps (the amount of sec it SHOULD take for one frame to render, even if it doesnt, will be the update_timestep)
 - update local simulations with local input immediately without waiting for ack from other player
 - both should send the input data at the fixed time_steps
 - input_data will come attached with a timestamp, which the client will use to determine the gamestate to rollback to in the buffer and resimulate with the added input
 - if client sends input and doesnt recieve an ack, resend the input
 -  only send full gamestates periodically to resync
 - when a player receives a new game state from the other player, compare it to their own game state and apply necessary corrections using interpolation techniques
    - this shifts the gamestates so that they resync over time
"""

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
                    if self.session_list_callback is not None:
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
                        self.game.player_2.pressed_keys = decoded_data["pressed_keys"]
                    else:  # recieved keys from host
                        self.game.player_1.pressed_keys = decoded_data["pressed_keys"]

                # gamestate update
                case 'update':
                    p1_data = decoded_data["player_1"]
                    p2_data = decoded_data["player_2"]
                    self.game.player_1.from_dict(p1_data)
                    self.game.player_2.from_dict(p2_data)
                    self.game.match_time = decoded_data["match_time"]

                # connection to host no longer active
                case 'disconnect':
                    self.game.lobby_view()
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

    def send_message(self, message, serialize=True):
        try:
            if serialize:
                message = json.dumps(message).encode('utf-8')
            self.sock.sendto(message, (self.server_ip, self.server_port))
        except Exception as e:
            print(f"Error while sending message to ({self.server_ip}, {self.server_port}): {e}\n Message: {message}")