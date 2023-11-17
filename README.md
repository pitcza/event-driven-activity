# Real-Time Chat App
Creating a simple real-time chat app using Python sockets and Tkinter involves building a server and a client, and then connecting them through a network. 

First, create two separate files for the server (`server.py`) and the client (`client.py`).

## Server Socket
1. Import socket and threading.
   Create server configuration, then assign the host IP Address and port number. Also add server limit and the function to store connected clients.
```python
HOST = '127.0.0.1'
PORT = 1100
LISTENER_LIMIT = 4
clients = []
```
2. ### Create main function
3. 
