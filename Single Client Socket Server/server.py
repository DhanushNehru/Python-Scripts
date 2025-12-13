import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #AF_INET for IPv4, SOCK_STREAM for TCP
    s.bind((HOST, PORT)) # Bind the socket to the address and port
    s.listen() # Enable the server to accept connections
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept() # Wait for a connection
    with conn: # conn is a new socket object usable to send and receive data
        print(f"Connected by {addr}") # Accept the connection
        while True: # Loop to handle incoming data
            data = conn.recv(1024) # Receive data from the connection
            if not data:
                break
            conn.sendall(data) # Echo the received data back to the client