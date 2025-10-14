
# Socket Communication - Single Client and Server

This project demonstrates basic socket programming in Python with a server and a single client. The server waits for a client to connect and then allows two-way communication between the server and the client.

## 📁 Files

- `server.py` – Runs the socket server and waits for a client to connect.
- `client.py` – Connects to the server and allows interaction with it.

## 🛠 Requirements

- Python 3.x
- No external libraries required (uses built-in `socket` module)

## 🚀 How to Run

> ⚠️ Make sure both scripts are in the same directory and run them in separate terminals.

### 1. Start the Server

Open a terminal and run:

```bash
python server.py
````

This will start the server on `localhost` and listen on a predefined port (usually `localhost:12345` unless configured otherwise).

### 2. Start the Client

In a **different terminal**, run:

```bash
python client.py
```

This will connect the client to the server.

Once connected, you can exchange messages between the server and the client.



## ❗ Notes

* Only **one client** is supported at a time.
* If you close either the server or client, the socket connection will be terminated.
* If the server crashes or is stopped, the client will also lose connection.


