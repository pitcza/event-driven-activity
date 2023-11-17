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

Create function to listen for upcoming messages from a client
```python
def broadcast(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f"The message send from client {username} is empty")
```

Create function that send message to a single client
```python
def send_message_to_client(client, message):
    client.sendall(message.encode())
```

Create a function that will send new messages to all the clients that are currently connected to the server
```python
def send_messages_to_all(message):
    for user in clients:
        send_message_to_client(user[1], message)
```

Use `client_handler()` function to handle every client that will join to the server
```python
def client_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} joined the chat app"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=broadcast, args=(client, username, )).start()
```
> This is a loop that waits for connected clients and then sends a joined chat app message that contains the username.

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
> This is a loop that waits for incoming connections and as soon as it gets one, it logs the connection (prints some of the connection details) and sends the connected client a message. It stores the client’s address in the addresses dictionary and later starts the handling thread for that client.

Put in code for starting the server and listening for incoming connections
```python
if __name__ == '__main__':
    main()
```
