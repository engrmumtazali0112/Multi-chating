import socket
import threading

# Server Configuration
HEADER_LENGTH = 10
IP = "0.0.0.0"  # Listen on all available interfaces
PORT = 5555
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(5)

# List of connected clients
clients = []

# Handle incoming messages from a client
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    while True:
        try:
            # Receive the message header
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                break

            # Get the message length
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"Received message from {client_address}: {message}")

            # Broadcast the message to all connected clients
            broadcast(message, client_socket)

        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove client from list if disconnected
    clients.remove(client_socket)
    client_socket.close()

# Broadcast message to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client.send(message_header + message.encode('utf-8'))
            except:
                # If client disconnected, remove from list
                clients.remove(client)

# Accept connections and create new threads
def start_server():
    print(f"Server started. Listening for connections on {IP}:{PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        # Start a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
