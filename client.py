import socket
import threading
import json
from button import Button

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

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.handle_message(data, addr)

    def handle_message(self, data, addr):
        decoded_data = json.loads(data.decode('utf-8'))

        match decoded_data["type"]:

            case 'session_list':
                print(decoded_data["sessions"])
                self.game.session_buttons = []
                for i, session in enumerate(decoded_data["sessions"]):
                    button = Button(100,40*i+30,100,50,30,session)
                    self.game.session_buttons.append(button)

            # gamestate update from server
            case 'UPDATE':
                pass

            # server no longer active
            case 'DISCONNECT':
                pass

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