# TCP Chat Server  

A simple TCP server that listens for client connections and receives messages. This server can be used with **Netcat (`nc`)** or any other TCP client.  

---

## 🚀 Features  
- Handles incoming client connections.  
- Receives messages in real-time.  
- Prevents address reuse errors (`OSError: Address already in use`).  
- Works with **Netcat (`nc`)** or any TCP client.  

---

## 🛠️ Installation & Setup  
- Navigate to 'TCP Chat Server' directory and run python3 server.py
- To test the connection open a new terminal and run nc localhost 3000
- Type the message here, it will be reflected in the first terminal