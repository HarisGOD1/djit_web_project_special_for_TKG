import random
import socket

# Define the server address and port
HOST = '127.0.0.1'  # Localhost or the IP of the machine running the server
PORT = 65399    # The same port the server is listening on

def send(data):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((HOST, PORT))

        # Send data to the server
        client_socket.sendall(data.encode())

        # Receive the response from the server
        response = client_socket.recv(1024)
        print(f"Received response: {response.decode()}")
        return response.decode()