import socket
import threading
import json

from server import Server

"""
This class represents the central Lobby server that
player can connect to at any time from the menu.
The game client will never create an instance of lobby;
rather, Lobby would be hosted on a dev's computer or via 
a hosting service.
"""

class Lobby(Server):
    def __init__(self):
        super().__init__()
        self.sessions = {}

    def handle_message(self, data, client):
        decoded_data = json.loads(data.decode('utf-8'))

        if decoded_data["type"] == "register_session":
            session_info = decoded_data.get("session_info")
            self.register_session(client, session_info)

        elif decoded_data["type"] == "list_sessions":
            self.send_sessions(client)

        elif decoded_data["type"] == "unregister_session":
            self.unregister_session(client)

    def register_session(self, client, session_info):
        self.sessions[client] = session_info
        print(f"Registered session: {session_info}")

    def unregister_session(self, client):
        if client in self.sessions:
            del self.sessions[client]
            print(f"Unregistered session: {client}")

    def send_sessions(self, client):
        print(f"Session list sent to {client}")
        sessions_list = list(self.sessions.values())
        response = {
            "type": "session_list",
            "sessions": sessions_list,
        }
        self.send_message(response, client)

if __name__ == "__main__":
    lobby = Lobby()
    lobby_thread = threading.Thread(target=lobby.listen)
    lobby_thread.start()
