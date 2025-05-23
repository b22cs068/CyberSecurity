import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate client's RSA key pair
client_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
client_public_key = client_private_key.public_key()

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

def start_client():
    # Create and connect the socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 65432))

    # Receive server's public key
    server_public_key_bytes = client_socket.recv(1024)
    server_public_key = serialization.load_pem_public_key(server_public_key_bytes)

    # Send client's public key to the server
    client_socket.send(client_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == "exit":
            break

        # Encrypt the message with the server's public key
        encrypted_message = encrypt_message(server_public_key, message)
        client_socket.send(encrypted_message)

        # Receive the encrypted response and decrypt it
        encrypted_response = client_socket.recv(1024)
        response = decrypt_message(client_private_key, encrypted_response)
        print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
