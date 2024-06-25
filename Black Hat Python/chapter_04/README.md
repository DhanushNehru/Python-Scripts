### mail_sniffer.py

- Install scapy package
```python
sudo pip3 install scapy
```
- A simple sniffer 
```
sudo python3 mail_sniffer.py
```

### mail_sniffer_using_BPF_syntax.py
- If you are on a network where you know you're already on their internal network and you want to compromise some mail server accounts then you could do that by sniffing the network by running the below command
```
sudo python3 mail_sniffer_using_BPF_syntax.py
```

### arper.py
```
python3 arper.py <victim_ip> <gateway_ip> <interface>
```