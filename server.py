import socket
import threading
import json

class Host:
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
            print(data)
            self.handle_message(data, addr)

    def handle_message(self, data, addr):
        data = json.loads(data.decode('utf-8'))
        # Handle incoming messages from clients
        # Update game state and broadcast it to all clients
        match data['type']:
            case 'JOIN':
                self.clients[addr] = data
                print(f"New client joined: {addr}")
                welcome_message = {
                    "Order": ["2", "bacon cheeseburger", "large strawberry lemonade", "large fry"]
                }
                self.send_message(json.dumps(welcome_message).encode('utf-8'), addr)

            case 'UPDATE':
                client_data = self.clients.get(addr)
                if client_data is not None:
                    client_data['data'] = data['data']
                    self.broadcast(client_data)

    def broadcast(self, data):
        for client_addr in self.clients:
            self.server_socket.sendto(json.dumps(data).encode('utf-8'), client_addr)

    def send_message(self, message, addr):
        self.sock.sendto(message, addr)

if __name__ == "__main__":
    # server public ip "73.247.171.208"
    server = Host("0.0.0.0", 8001)
    server.listen()