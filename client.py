import socket
import threading

class Client:
    def __init__(self, server_ip, server_port, local_ip, local_port):
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
        print(data)

    def send_message(self, message):
        self.sock.sendto(message, (self.server_ip, self.server_port))

    def join(self):
        data = {
            'type': 'JOIN',
            'data': {
                'username': 'Player1'
            }
        }
        self.client_socket.sendto(json.dumps(data).encode('utf-8'), (self.ip, self.port))

    def update(self, data):
        data = {
            'type': 'UPDATE',
            'data': data
        }
        self.client_socket.sendto(json.dumps(data).encode('utf-8'), (self.ip, self.port))

if __name__ == "__main__":
    client = Client(server_ip, server_port, local_ip, local_port)