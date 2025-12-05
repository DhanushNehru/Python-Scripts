import psutil
import ipaddress

def get_network_info():
    network_info = {}
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            # 2 represents IPv4
            if addr.family == 2:
                # Collect information only for IPv4 addresses
                network_info[interface] = (addr.address, addr.netmask, addr.broadcast)
    return network_info

def calculate_subnet_details(ip, netmask):
    # Convert IP and netmask to ipaddress objects
    network = ipaddress.ip_network(f"{ip}/{netmask}", strict=False)
    subnet = network.network_address
    broadcast = network.broadcast_address
    first_usable_ip = subnet + 1
    last_usable_ip = broadcast - 1
    return subnet, broadcast, first_usable_ip, last_usable_ip

def main():
    network_info = get_network_info()

    for interface, (ip, netmask, broadcast) in network_info.items():
        subnet, broadcast, first_usable_ip, last_usable_ip = calculate_subnet_details(ip, netmask)
        print(f"Interface: {interface}")
        print(f"IP Address: {ip}")
        print(f"Subnet: {subnet}")
        print(f"Netmask: {netmask}")
        print(f"Range of IP addresses: {subnet} - {broadcast}")
        print(f"Usable Range of IPs: {first_usable_ip} - {last_usable_ip}")
        print(f"Broadcast: {broadcast}")
        print()

if __name__ == "__main__":
    main()
