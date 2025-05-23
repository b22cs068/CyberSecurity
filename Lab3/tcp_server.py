import socket

# Define server IP and port
SERVER_IP = "0.0.0.0"  # Listen on all available interfaces
SERVER_PORT = 5001  # Change port for different runs

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

print(f"[*] Server listening on {SERVER_IP}:{SERVER_PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"[+] Connection received from {client_address}")

    # Receive data
    data = client_socket.recv(1024).decode()
    print(f"[*] Received: {data}")

    # Send a response
    response = "Hello from Server!"
    client_socket.send(response.encode())

    # Close connection
    client_socket.close()
