### sniffer_basic.py

```bash
sudo python3 sniffer_basic.py 
```
If running in local machine input the ip address which can be got by running `ipconfig` on Windows and `ipconfig getifaddr en0` on macOS

Open another terminal pick a host to ping.
```bash
ping google.com 
```
Then you should see some garbled output 

### sniffer_ip_header_decode.py

```bash
sudo sniffer_ip_header_decode.py 
```
Open another terminal pick a host to ping.
```bash
ping google.com 
```
We would be able to see only the response and only for the ICMP protocol

### sniffer_with_icmp.py

```bash
sudo python3 sniffer_with_icmp.py
```
Open another terminal pick a host to ping.
```bash
ping google.com 
```

The output actually indicates that the ping (ICMP Echo) responses are being correctly received and decoded

### scanner.py

This code scans a specified subnet for active hosts by sending UDP datagrams and listening for ICMP "port unreachable" responses to identify which hosts are up. It prints the IP addresses of responsive hosts within the given subnet
```bash
sudo python3 scanner.py 192.168.1.0

# subnet to target: 192.168.1.0/24 
```

<!-- Updated README links and corrected typos -->
<!-- Updated README links and corrected typos -->