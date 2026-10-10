import ipaddress


def calculate_network_info(ip_address, subnet_mask):
    network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)

    network_address = network.network_address
    broadcast_address = network.broadcast_address
    total_hosts = network.num_addresses
    usable_hosts = max(total_hosts - 2, 0)
    first_usable_host = network_address + 1 if usable_hosts > 0 else None
    last_usable_host = broadcast_address - 1 if usable_hosts > 0 else None

    results = {
        "IP Address": ip_address,
        "Subnet Mask": subnet_mask,
        "Network Address": str(network_address),
        "Broadcast Address": str(broadcast_address),
        "Range of IP addresses": f"{network_address} - {broadcast_address}",
        "Usable Host IP Range": (
            f"{first_usable_host} - {last_usable_host}" if usable_hosts > 0 else "N/A"
        ),
        "Total Hosts": total_hosts,
        "Usable Hosts": usable_hosts,
    }

    return results


def main():
    try:
        ip_address = input("Enter IP address: ")
        subnet_mask = input("Enter subnet mask: ")

        info = calculate_network_info(ip_address, subnet_mask)

        print("\nNetwork Information:")
        for key, value in info.items():
            print(f"{key}: {value}")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
