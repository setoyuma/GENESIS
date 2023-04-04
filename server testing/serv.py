import socket
import threading

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listen_thread.start()
    
    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print("Data Recieved: ", data.decode('utf-8'))
            recv_msg = f"Welcome To The Server {data}!"
            self.sock.sendto(recv_msg.encode('utf-8'), addr)



UDP_IP = "127.0.0.1"  # Replace with your own IP address
UDP_PORT = 5005  # Replace with your own port number

server = Server(UDP_IP, UDP_PORT)
server.listen()