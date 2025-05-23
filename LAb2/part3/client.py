import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate client keys
client_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
client_public_key = client_private_key.public_key()

# Encrypt function
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

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 65432))

# Receive server's public key
server_public_key_data = client.recv(4096)
server_public_key = serialization.load_pem_public_key(server_public_key_data)

# Send the client's public key to the server
client.send(client_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
))

while True:
    message = input("Enter message to send to server: ").strip().lower()
    if message == "exit":
        break

    # Encrypt the message with the server's public key
    encrypted_message = encrypt_with_public_key(server_public_key, message.encode())
    client.send(encrypted_message)

    # Receive and decrypt the response from the server
    encrypted_response = client.recv(4096)
    response = decrypt_with_private_key(client_private_key, encrypted_response).decode()

    print(f"Response from server: {response}")

client.close()
