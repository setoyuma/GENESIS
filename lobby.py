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
        self.id_counter = 1

    def handle_message(self, data, client):
        decoded_data = json.loads(data.decode('utf-8'))

        if decoded_data["type"] == "register_session":
            session_info = decoded_data.get("session_info")
            self.register_session(client, session_info)

        elif decoded_data["type"] == "list_sessions":
            self.send_sessions(client)

        elif decoded_data["type"] == "unregister_session":
            self.unregister_session(client)
        
        elif decoded_data["type"] == "join_session":
            for session in self.sessions.values():
                if session["id"] == decoded_data["id"]:
                    session_info = session
            data = {
                "type": "session_info",
                "session": session_info
            }
            self.send_message(data, client)

        elif decoded_data["type"] == "disconnect":
            self.disconnect(client)

    def register_session(self, client, session_info):
        # give the session an id
        session_info["id"] = self.id_counter
        self.id_counter += 1

        # add host to the client list
        session_info["clients"] = client

        # add it to the sessions dict
        self.sessions[client] = session_info
        print(f"Registered session: {session_info}")

    def send_sessions(self, client):
        print(f"Session list sent to {client}")
        sessions_list = list(self.sessions.values())
        response = {
            "type": "session_list",
            "sessions": sessions_list,
        }
        self.send_message(response, client)

    def unregister_session(self, client):
        if client in self.sessions:
            print(f"Unregistered session: {self.sessions[client]}")
            del self.sessions[client]


if __name__ == "__main__":
    lobby = Lobby()
    lobby_thread = threading.Thread(target=lobby.listen)
    lobby_thread.start()
