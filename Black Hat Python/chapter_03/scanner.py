import ipaddress
import os
import socket
import struct
import sys
import threading
import time

# Function to get subnet input from user
def get_subnet():
    while True:
        subnet = input("Enter the subnet to target (e.g., 192.168.1.0/24): ")
        try:
            # Validate the subnet input
            ipaddress.ip_network(subnet)
            return subnet
        except ValueError:
            print("Invalid subnet. Please try again.")

# Magic string we'll check ICMP responses for
MESSAGE = 'PYTHONRULES!'

# Class to handle IP headers
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

        # Convert binary IP addresses to human-readable format
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # Map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except KeyError:
            print('No protocol for %s' % self.protocol_num)
            self.protocol = str(self.protocol_num)

# Class to handle ICMP headers
class ICMP:
    def __init__(self, buff):
        # Unpack the ICMP header fields from the buffer
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

# Function to send UDP datagrams with our magic message
def udp_sender(subnet):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        # Send datagrams to all hosts in the subnet
        for ip in ipaddress.ip_network(subnet).hosts():
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 65212))

# Class to handle the scanning and sniffing process
class Scanner:
    def __init__(self, host):
        self.host = host
        # Choose the correct protocol based on the OS
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        # Create a raw socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # Enable promiscuous mode on Windows
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self, subnet):
        # Set to keep track of hosts that are up
        hosts_up = set([f'{str(self.host)} *'])
        try:
            while True:
                # Read a packet
                raw_buffer = self.socket.recvfrom(65535)[0]

                # Create an IP header from the first 20 bytes
                ip_header = IP(raw_buffer[0:20])

                # If it's ICMP, we want it
                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)

                    # Check for TYPE 3 and CODE 3
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        # Ensure the response is in our target subnet
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(subnet):
                            # Make sure it has our magic message
                            if raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                                if str(ip_header.src_address) not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    print(f'Host Up: {ip_header.src_address}')
        except KeyboardInterrupt:
            # Disable promiscuous mode on Windows
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

            print('\nUser interrupted.')
            if hosts_up:
                print(f'\n\nSummary: Hosts up on {subnet}')
                for host in sorted(hosts_up):
                    print(f'{host}')
            print('')
            sys.exit()

if __name__ == '__main__':
    # Get the target subnet from the user
    SUBNET = get_subnet()

    # Determine the host to bind to
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)

    print("Using host:", host)

    # Create a scanner instance
    s = Scanner(host)

    # Start the UDP sender in a separate thread
    t = threading.Thread(target=udp_sender, args=(SUBNET,))
    t.start()

    # Start sniffing
    s.sniff(SUBNET)