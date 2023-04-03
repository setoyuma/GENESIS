import socket

UDP_IP = "127.0.0.1"  # Replace with the IP address of the server
UDP_PORT = 5005  # Replace with the port number of the server
username = input("Type A Username:")
MESSAGE = f"{username}!"  # Replace with your own message

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))  # Send the message to the server
data, addr = sock.recvfrom(1024)  # Receive the response from the server
print("Received message:", data)  # Print the received message
