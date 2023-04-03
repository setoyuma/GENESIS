import json

from server import Server

"""
This class turns a basic client into a host
server. An instance of this is created when
a player creates a session using the lobby.

1. Player starts the game
2. Game creates an instance of Client
3. Player clicks 'create lobby'
4. The game replaces its current Client object with a Host object
5. The host client sends a message to the lobby server asking for session registration
6. Another client decides to join the session
7. Host starts the match
8. The clients exchange information with each other through the lobby server using STUN
9a. The clients initiate a direct connection with each other
9b (OPTIONAL) If a direct connection is not possible, use the lobby server as a relay
10a. The player 2 client sends events to the host
10b. The player 1 client manages the gamestate and sends it to player 2
"""

class Host(Server):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def handle_message(self, data, client):
        decoded_data = json.loads(data.decode('utf-8'))

        match decoded_data["type"]:

            # gamestate update from server
            case 'UPDATE':
                pass