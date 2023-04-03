import socket
import threading
import json

"""
This class provides the base capabilities for
sending and receiving messages over the internet.
"""

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.clients = {}
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listen_thread.start()

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.handle_message(data, addr)

    # overwrite this method
    def handle_message(self, data, addr):
        pass

    def broadcast(self, data):
        for client_addr in self.clients:
            self.server_socket.sendto(json.dumps(data).encode('utf-8'), client_addr)

    def send_message(self, message, addr):
        self.sock.sendto(json.dumps(message).encode('utf-8'), addr)

if __name__ == "__main__":
    # server public ip "73.247.171.208"
    server = Host("0.0.0.0", 8001)
    server.listen()