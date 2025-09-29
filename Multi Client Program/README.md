# Multi-Client Chat Application (Python)

This is a simple **Client-Server Chat Program** written in Python.  
It allows multiple clients (running from different terminals) to connect to a single server and exchange messages in real-time.



## Features
- Multi-client support (multiple users can chat at the same time)
- Real-time message broadcasting (messages from one client are sent to all connected clients)
- Simple terminal-based interface
- Implemented using **Python sockets** and **threading**


## Project Structure
``` text
multi_client_chat/
│
├── server.py 
│
├── client.py 
│
├── output/
│ └── image.png 
│
└── README.md 
```


## How It Works
1. The **server** (`server.py`) runs and listens for incoming client connections.  
2. Each new client (`client.py`) connects to the server.  
3. The server uses threading to handle multiple clients simultaneously.  
4. Messages sent by a client are broadcast to all other connected clients.



## Requirements
- Python 3.x installed on your system  
- Multiple terminals (or command prompts) to run server and clients simultaneously



## How to Run

### 1. Start the Server  
Open a terminal and run:  
``` bash
python server.py
```
The server will start and wait for clients to connect.

### 2. Start a Client  
Open another terminal (or multiple terminals for multiple users) and run:  
```bash
python client.py
```
### 3. Start Chatting  
Type a message in a client terminal and press Enter.  
The message will be broadcast to all connected clients.

## Notes
- You can change the host and port in both `server.py` and `client.py` if needed.  
- This program works on the same machine (localhost) or across different machines in the same network (replace `127.0.0.1` with the server IP address).

## License
This project is for educational purposes only. Feel free to modify and improve it.