import ipaddress
import os
import socket
import struct
import sys

# Define a class to represent the IP header of a packet
class IP:
    def __init__(self, buff=None):
        # Unpack the IP header fields from the buffer
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF
        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # Convert source and destination IP addresses to human-readable format
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # Map protocol numbers to protocol names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No protocol for %s' % (e, self.protocol_num))
            self.protocol = str(self.protocol_num)

# Define a class to represent the ICMP header of a packet
class ICMP:
    def __init__(self, buff):
        # Unpack the ICMP header fields from the buffer
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

# Function to sniff packets on a specified host
def sniff(host):
    # Determine the appropriate socket protocol
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    # Create a raw socket and bind it to the host
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # If running on Windows, set the socket to promiscuous mode
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            # Read a packet
            raw_buffer = sniffer.recvfrom(65535)[0]

            # Create an IP header from the first 20 bytes of the packet
            ip_header = IP(raw_buffer[0:20])

            # If the packet is ICMP, process and print its details
            if ip_header.protocol == "ICMP":
                print('Protocol: %s %s -> %s' % (
                    ip_header.protocol,
                    ip_header.src_address,
                    ip_header.dst_address))
                print(f'Version: {ip_header.ver}')
                print(f'Header Length: {ip_header.ihl} TTL: {ip_header.ttl}')

                # Calculate the starting point of the ICMP packet
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + 8]

                # Create an ICMP header from the buffer
                icmp_header = ICMP(buf)
                print('ICMP -> Type: %s Code: %s\n' % (icmp_header.type, icmp_header.code))
    except KeyboardInterrupt:
        # If running on Windows, turn off promiscuous mode
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()

if __name__ == '__main__':
    # If a host is specified in command-line arguments, use it
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        # Otherwise, get the local machine's IP address
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
    print("Using host:", host)
    # Start sniffing packets on the specified host
    sniff(host)