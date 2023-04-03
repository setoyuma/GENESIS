import socket

UDP_IP = "127.0.0.1"  # Replace with your own IP address
UDP_PORT = 5005  # Replace with your own port number

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
sock.bind((UDP_IP, UDP_PORT))  # Bind the socket to the IP address and port

while True:
    data, addr = sock.recvfrom(1024)  # Receive data from a client
    print("Received message:", data)  # Print the received message
    sock.sendto(data.upper(), addr)  # Send a response back to the client
