import socket
target_host = "127.0.0.1"
target_port = 9998

# create a socket object
# AF_INET parameter indicates we’ll use a standard IPv4 address or hostname
# SOCK_DGRAM indicates that this will be a UPD client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
client.sendto(b"AAABBBCCC",(target_host,target_port))
# receive some data
data, addr = client.recvfrom(4096)
print(data.decode())
client.close()