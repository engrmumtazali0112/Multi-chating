import socket
import threading

# Server Configuration
HEADER_LENGTH = 10
IP = "192.168.13.182"  # Update with the server's IP
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(5)

clients = []

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    while True:
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not message_header:
                break
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            print(f"Received: {message} from {client_address}")
        except Exception as e:
            print(f"Error: {e}")
            break
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    print(f"Server running on {IP}:{PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if _name_ == "_main_":
    start_server()
