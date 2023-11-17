# Real-Time Chat App
Creating a simple real-time chat app using Python sockets and Tkinter involves building a server and a client, and then connecting them through a network. 

First, create two separate files for the server (`server.py`) and the client (`client.py`).

## Server Socket
Import socket and threading.
```python
import socket
import threading
```

Create server configuration, then assign the host IP address and port number. Also add server limit and the function to store connected clients.
```python
HOST = '127.0.0.1'
PORT = 1100
LISTENER_LIMIT = 4
clients = []
```
### Create main function
```python
def main():
```
1. Include the Socket class. A socket object represents the pair of host address and port number. Use TCP sockets for this purpose, so use AF_INET and SOCK_STREAM flags.
```python
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
2. Use `bind()` method to bind the socket to a specific address and port.
```python
   try:
        server.bind((HOST, PORT))
        print(f"Server listening on {HOST} : {PORT}")
    except:
        print(f"Unable to bind host {HOST} and port {PORT}")
```
3. Set the server limit.
```python
server.listen(LISTENER_LIMIT)
```
4. Create function that will listen to client connections.
```python
   while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()
```
### Create function listen for upcoming messages from a client
