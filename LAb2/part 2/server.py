import socket
if __name__=="__main__":
    ip="127.0.0.1"
    port= 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((ip,port))
    
    message=" Hello, SErver! THis is CLient"
    server_socket.send(message.encode())
    
    response = server_socket.recv(1024).decode()
    print(f"Server says :{response}")
    server_socket.close()
    print(f"connection closed")