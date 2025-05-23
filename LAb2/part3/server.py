import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate server keys
server_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
server_public_key = server_private_key.public_key()

# Encrypt Function
def encrypt_with_public_key(public_key, message):
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Decrypt Function
def decrypt_with_private_key(private_key, ciphertext):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 65432))
server.listen(1)
print("Server listening on port 65432...")

client_socket, client_address = server.accept()
print(f"Connection established with {client_address}")

# Send the server's public key to the client
client_socket.send(server_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
))

# Receive client's public key
client_public_key_data = client_socket.recv(4096)
client_public_key = serialization.load_pem_public_key(client_public_key_data)

while True:
    encrypted_message = client_socket.recv(4096)
    if not encrypted_message:
        break

    # Decrypt the client's message
    message = decrypt_with_private_key(server_private_key, encrypted_message).decode()

    # Prepare the response (echo + uppercase + reverse order)
    response = f"""{message}
{message.upper()}
{message[::-1]}"""

    # Encrypt the response with the client's public key
    encrypted_response = encrypt_with_public_key(client_public_key, response.encode())
    client_socket.send(encrypted_response)

client_socket.close()
server.close()