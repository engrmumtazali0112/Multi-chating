import socket
import threading
import sys

# Constants
HEADER_LENGTH = 10
IP = "192.168.43.165"  # Server IP Address (update with the correct server IP)
PORT = 5555
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

# Username input
my_username = input("Enter your username: ")

# Sending the username to the server
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# Function to receive messages from other clients
def receive_messages():
    while True:
        try:
            # Receive the message header
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                break

            # Get the message length and then the actual message
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"\nNew message: {message}")

        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Function to send messages to the server
def send_message():
    while True:
        message = input(f"{my_username}: ")
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

if __name__ == "__main__":
    # Start receiving messages in a separate thread
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    # Start sending messages
    send_message()
