import socket

IP = '0.0.0.0'
PORT = 3000

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))

    server.listen(5)
    print(f'Server is listening on {IP}:{PORT}')

    while True:
        client, address = server.accept()
        print(f'Received a connection from {address[0]}:{address[1]}')
        
        data = client.recv(4096)
        decoded_data = data.decode()
        print(decoded_data)

        send = input('Send message> ')
        client.send(send.encode())


if __name__ == '__main__':
    main()
