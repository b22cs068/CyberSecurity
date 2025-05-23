import socket

if __name__=="__main__":

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 1234

    server_socket.bind((host, port))

    server_socket.listen(5)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection EStablished with {client_address[0]}:{client_address[1]}")

        data = client_socket.recv(1024).decode()
        print(f"Client says: {data}")

        response = "HEllo, CLient!HAndshake successsful"
        client_socket.send(response.encode())

        client_socket.close()
        print("COnnection closed")