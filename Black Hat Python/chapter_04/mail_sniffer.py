from scapy.all import sniff

# Callback function that is called for each packet sniffed
def packet_callback(packet):
    # Display the packet details
    packet.show()

def main():
    # Sniff one packet and call packet_callback for each packet sniffed
    sniff(prn=packet_callback, count=1)

if __name__ == '__main__':
    main()