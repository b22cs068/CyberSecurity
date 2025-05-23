import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate server's RSA key pair
server_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
server_public_key = server_private_key.public_key()

# Generate client's public key (shared during communication)
client_public_key = None

# Encrypt a message with a public key
def encrypt_message(public_key, message):
    return public_key.encrypt(
        message.encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

# Decrypt a message with a private key
def decrypt_message(private_key, encrypted_message):
    return private_key.decrypt(
        encrypted_message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    ).decode()

def start_server():
    global client_public_key

    # Create and bind the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 65432))
    server_socket.listen(1)
    print("Server is listening on port 65432...")

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    # Share server's public key with the client
    conn.send(server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    # Receive and load the client's public key
    client_public_key_bytes = conn.recv(1024)
    client_public_key = serialization.load_pem_public_key(client_public_key_bytes)

    while True:
        encrypted_data = conn.recv(1024)
        if not encrypted_data:
            break

        # Decrypt the received message
        received_message = decrypt_message(server_private_key, encrypted_data)
        print(f"Received from client: {received_message}")

        # Perform different operations
        if received_message == "echo":
            response = "ECHO"
        elif received_message.islower():
            response = received_message.upper()
        else:
            response = received_message[::-1]

        # Encrypt the response with the client's public key
        encrypted_response = encrypt_message(client_public_key, response)
        conn.send(encrypted_response)

    conn.close()

if __name__ == "__main__":
    start_server()
