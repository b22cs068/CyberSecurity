import socket

# Define server details
SERVER_IP = "127.0.0.1"  # Change if server is on a different machine
SERVER_PORT = 5001  # Must match server port

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Send a message
message = "Hello from Client!"
client_socket.send(message.encode())

# Receive response
response = client_socket.recv(1024).decode()
print(f"[*] Server Response: {response}")

# Close connection
client_socket.close()
