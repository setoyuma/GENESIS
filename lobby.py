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

    def get_session(self, id):
        for host_client, session in self.sessions.items():
            if session["id"] == id:
                return host_client, session

    def handle_message(self, data, client):
        decoded_data = json.loads(data.decode('utf-8'))

        if decoded_data["type"] == "register_session":
            session_info = decoded_data.get("session_info")
            self.register_session(client, session_info)

        # a client is fetching the session list
        elif decoded_data["type"] == "list_sessions":
            self.send_sessions(client)

        # host has left their session
        elif decoded_data["type"] == "unregister_session":
            self.unregister_session(client)
        
        # guest joined a host's session
        elif decoded_data["type"] == "join_session":
            self.join_session(decoded_data, client)
        
        # host has initiated a handshake with guest
        elif decoded_data["type"] == "handshake":
            self.send_message({"type": "handshake"}, self.sessions[client]["clients"][1])  # tells Guest to finish the handshake

        # guest has left the session
        elif decoded_data["type"] == "disconnect":
            self.disconnect(client)

    def register_session(self, client, session_info):
        # give the session an id
        session_info["id"] = self.id_counter
        self.id_counter += 1
        # add host to the client list
        session_info["clients"] = client
        # add joinable flag
        session_info["joinable"] = True
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

    def join_session(self, decoded_data, client):
        key, session_info = self.get_session(decoded_data["id"])
        self.sessions[key]["joinable"] = False  # a 2nd player has just joined, filling the session
        self.sessions[key]["clients"].append(client)  # guest client is added to the session clients
        data = {"type": "session_info", "session": session_info}
        for client in session_info["clients"]:
            self.send_message(data, client)  # send the session information to both clients

    def disconnect(self, client, decoded_data):
        key, session = self.get_session(decoded_data["id"])
        self.sessions[key]["clients"] = [key]  # remove guest from session
        data = {"type": "session_info", "session": session_info}
        self.send_message(data, key)  # refresh host's session info


if __name__ == "__main__":
    lobby = Lobby()
    lobby_thread = threading.Thread(target=lobby.listen)
    lobby_thread.start()
