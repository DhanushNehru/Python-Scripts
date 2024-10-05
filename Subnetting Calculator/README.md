# Subnetting Calculator

This Python script calculates network information based on a given IP address and subnet mask.

## Features

- Calculates network address and broadcast address
- Provides the range of IP addresses for the network
- Shows the usable host IP range
- Calculates the total number of hosts and usable hosts

## Usage

1. Ensure you have Python 3.x installed on your system.
2. Run the script:
   ```
   python subnetting_calculator.py
   ```
3. Enter the IP address and subnet mask when prompted.

## Example

```
Enter IP address: 192.168.1.1
Enter subnet mask: 255.255.255.0

Network Information:
IP Address: 192.168.1.1
Subnet Mask: 255.255.255.0
Network Address: 192.168.1.0
Broadcast Address: 192.168.1.255
Range of IP addresses: 192.168.1.0 - 192.168.1.255
Usable Host IP Range: 192.168.1.1 - 192.168.1.254
Total Hosts: 256
Usable Hosts: 254
```

## Requirements

This script uses the `ipaddress` module, which is part of the Python standard library. No additional installations are required.
