
"""
This class turns a basic client into a host
server. An instance of this is created when
a player creates a session using the lobby.

1. Player starts the game
2. Game creates an instance of Client
3. Player clicks 'create lobby'
4. The game replaces its current Client object with a Host object
5. The host client sends a message to the lobby server asking for session registration
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