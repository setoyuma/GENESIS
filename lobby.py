import socket
import threading
import json
import time

from server import Server

"""
This class represents the central Lobby server that
players can connect to at any time from the menu.
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

    def handle_timeout(self, client):
        print(f"Client {client} has been timed out.")
        if client in self.sessions:
            self.unregister_session(client)

    def handle_message(self, data, client):
        try:
            decoded_data = json.loads(data.decode('utf-8'))

            # client keep-alive message
            if decoded_data["type"] == "heartbeat":
                with self.clients_lock:
                    self.clients[client] = time.time()

            # a client created a session
            elif decoded_data["type"] == "register_session":
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
                self.disconnect(client, decoded_data)

        except Exception as e:
            print(f"Error while handling message from {client}: {e}\n Data: {data}")

    # send the session list to a single client
    def send_sessions(self, client):
        sessions_list = list(self.sessions.values())
        data = {"type": "session_list", "sessions": sessions_list}
        self.send_message(data, client)
        print(f"Session list sent to {client}.")

    # send the session list to all clients
    def broadcast_session_list(self):
        sessions_list = list(self.sessions.values())
        data = {"type": "session_list", "sessions": sessions_list,}
        self.broadcast(data)
        print(f"Session list broadcasted to {len(self.clients)} clients.")

    # a client has created a session
    def register_session(self, client, session_info):
        # give the session an id
        session_info["id"] = self.id_counter
        self.id_counter += 1
        # add host to the client list
        session_info["clients"] = [client]
        # add it to the sessions dict
        self.sessions[client] = session_info
        self.broadcast_session_list()
        print(f"Registered session: {session_info}")

    # a host has cancelled their session
    def unregister_session(self, client):
        if client in self.sessions:
            if len(self.sessions[client]["clients"]) == 2:
                guest_client = self.sessions[client]["clients"][1]
                self.send_message({"type": "disconnect"}, guest_client)  # tell guest that the session is no longer available
            print(f"Unregistered session: {self.sessions[client]}")
            del self.sessions[client]
            self.broadcast_session_list()

    # put guest into a host's session
    def join_session(self, decoded_data, client):
        key, session_info = self.get_session(decoded_data["id"])
        if client == key or len(session_info["clients"]) >= 2:
            return  # host re-joining their own sesion before connection is timed out or session is full  
        self.sessions[key]["joinable"] = False  # will be used for password protected sessions
        self.sessions[key]["clients"].append(client)  # guest client is added to the session clients
        data = {"type": "session_info", "session": self.sessions[key]}
        for client in self.sessions[key]["clients"]:
            self.send_message(data, client)  # send the session information to both clients

    # disconnect guest from a host's session
    def disconnect(self, client, decoded_data):
        key, session = self.get_session(decoded_data["id"])
        self.sessions[key]["clients"] = [client]  # remove guest from session
        data = {"type": "session_info", "session": self.sessions[key]}
        self.send_message(data, key)  # refresh host's session info


if __name__ == "__main__":
    lobby = Lobby()
    lobby.listen()
