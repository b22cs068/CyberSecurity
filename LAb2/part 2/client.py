import socket

def connect_to_server():
    # Define the server's hostname and port
    hostname = "iitj.ac.in"
    port = 80  # HTTP port

    try:
        # Resolve the hostname to an IP address
        server_ip = socket.gethostbyname(hostname)
        print(f"Connecting to {hostname} ({server_ip}) on port {port}...")

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((server_ip, port))
        print(f"Connected to {hostname} successfully.")

        # Send an HTTP GET request
        request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
        client_socket.send(request.encode())

        # Receive the response
        response = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk

        # Print the response (first 1000 characters)
        print("Server Response:\n")
        print(response.decode("utf-8", errors="ignore")[:1000])  # Limit output for readability

        # Close the connection
        client_socket.close()
        print("\nConnection closed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    connect_to_server()
