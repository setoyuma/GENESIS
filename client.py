import socket
import threading
import json

class Client:
    def __init__(self, game, server_ip, server_port, local_ip, local_port):
        self.game = game
        self.server_ip = server_ip
        self.server_port = server_port
        self.local_ip = local_ip
        self.local_port = local_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.local_ip, self.local_port))
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listen_thread.start()

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.handle_message(data, addr)

    def handle_message(self, data, addr):
        decoded_data = json.loads(data)

        match decoded_data["type"]:

            case 'session_list':
                self.game.sessions = decoded_data["sessions"]
                
                

        print(data)

    def send_message(self, message):
        self.sock.sendto(json.dumps(message).encode('utf-8'), (self.server_ip, self.server_port))

    def join(self):
        data = {
            'type': 'JOIN',
            'data': {
                'username': 'Player1'
            }
        }
        self.sock.sendto(json.dumps(data).encode('utf-8'), (self.server_ip, self.server_port))

    def update(self, data):
        data = {
            'type': 'UPDATE',
            'data': data
        }
        self.sock.sendto(json.dumps(data).encode('utf-8'), (self.ip, self.port))

if __name__ == "__main__":
    client = Client("73.195.98.40", 3000, "10.0.0.29", 5000)
    client.join()
    client.listen()