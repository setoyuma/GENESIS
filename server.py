import socket
import threading
import json
import time


class Server:
    def __init__(self):
        self.ip =  self.get_ip() #local_ip
        self.port = 8001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.clients = {}
        self.clients_lock = threading.Lock()  # Add a lock for thread-safe access to self.clients
        self.timeout_thread = threading.Thread(target=self.check_timeouts, daemon=True)
        self.timeout_thread.start()

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

    def check_timeouts(self):
        heartbeat_timeout = 10  # seconds

        while True:
            time.sleep(1)  # Check timeouts every second
            current_time = time.time()

            with self.clients_lock:
                clients_to_remove = []

                for client, last_received in self.clients.items():
                    if current_time - last_received > heartbeat_timeout:
                        clients_to_remove.append(client)

                for client in clients_to_remove:
                    self.handle_timeout(client)
                    del self.clients[client]

    # overwrite this method
    def handle_timeout(self, client):
        pass

    # overwrite this method
    def handle_message(self, data, addr):
        pass

    def broadcast(self, data):
        for client_addr in self.clients:
            self.send_message(data, client_addr)

    def send_message(self, message, addr, serialize=True):
        try:
            if serialize:
                message = json.dumps(message).encode('utf-8')
            self.sock.sendto(message, addr)
        except Exception as e:
            print(f"Error while sending message to {addr}: {e}\n Message: {message}")


if __name__ == "__main__":
    server = Server()
    server.listen()