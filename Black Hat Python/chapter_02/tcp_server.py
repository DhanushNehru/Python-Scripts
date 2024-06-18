import socket
import threading

IP = '0.0.0.0'
PORT = 9998

def main():
    # AF_INET parameter indicates we’ll use a standard IPv4 address or hostname
    # SOCK_STREAM indicates that this will be a TCP client
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))  # Bind the socket to the address
    server.listen(5)  # Listen for incoming connections with a backlog of 5

    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        client, address = server.accept()  # Accept a new connection
        print(f'[*] Accepted connection from {address[0]}: {address[1]}')

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()  # Start a new thread to handle the client

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')  # Send an acknowledgement message

if __name__ == '__main__':
    main()
