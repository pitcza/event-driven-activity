# Real-Time Chat App
Creating a simple real-time chat app using Python sockets and Tkinter involves building a server and a client, and then connecting them through a network. 

First, create two separate files for the server (`server.py`) and the client (`client.py`).

## Server Socket (`server.py`)
Import socket and threading
```python
import socket
import threading
```

Create server configuration, then assign the host IP address and port number. Also, add the server limit and the function to store connected clients.
```python
HOST = '127.0.0.1'
PORT = 1100
LISTENER_LIMIT = 4
clients = []
```
> The server listens for incoming connections on IP address '127.0.0.1' and port 1100.

Create a function to listen for upcoming messages from a client.
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

Create a function to send message to a single client.
```python
def send_message_to_client(client, message):
    client.sendall(message.encode())
```

Create a function that will send new messages to all the clients that are currently connected to the server.
```python
def send_messages_to_all(message):
    for user in clients:
        send_message_to_client(user[1], message)
```

Use `client_handler()` function to handle every client that will join to the server.
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

> When the user enters a username and clicks the submit button, the `connect` function is called, which sends the username to the server using the established socket connection.

### Create main function
```python
def main():
```
1. Include the socket class. A socket object represents the pair of host address and port number. Use TCP sockets for this purpose, so use AF_INET and SOCK_STREAM flags.
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
4. Create a function that will listen to the client connections.
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



## Client Socket (`client.py`)
Import socket and threading, then use Tkinter, Python’s “batteries included” GUI building tool for our purpose.
```python
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
```

Assign styles for GUI.
```python
CY = '#00ABB3'
BG_DARK = '#3C4048'
GREY = '#B2B2B2'
WHITE = "white"
FONT = ("Tahoma", 13)
BUTTON_FONT = ("Tahoma", 11)
SMALL_FONT = ("Tahoma", 10)
```
> This is optional, and you can customize your GUI style.

Create a configuration and include the socket class. Like the server socket object, use TCP sockets for this purpose, so use AF_INET and SOCK_STREAM flags.
```python
HOST = '127.0.0.1'
PORT = 1100
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Create a function that will send an add-user message to the message box.
```python
def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)
```

Create a function that will connect clients to the server.
```python
def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)
```
> This is a try-except block to print some connected details message to the server's message box.

Create a function that will get the user's message from the message textbox.
```python
def send_message(event=None):
    message = message_textbox.get()
    client.sendall(message.encode())
    message_textbox.delete(0, len(message))
```
> Use the event as an argument because it is implicitly passed by Tkinter when the send button on the GUI is pressed.

> `message_textbox` is the input field on the GUI, and therefore we extract the message to be sent using `message = message_textbox.get()`. After that, we clear the input field and then send the message to the server, which, as we’ve seen before, broadcasts this message to all the clients.

Create a function that will receive client's messages and then send it to the server's message box.
```python
def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]
            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")
```
> This loop sends messages to the message box with the client's username included after it waits for incoming messages.

> Use an infinite loop because the server will be receiving messages quite non-deterministically.

Set up the GUI.

The client uses Tkinter to create a simple GUI with a label, an input widget, and a submit button.
```python
root = tk.Tk()
root.geometry("400x400")
root.resizable(False, False)
root.title("Real-Time Chat App")

top_frame = tk.Frame(root, width=400, height=100, bg=CY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=400, height=270, bg=BG_DARK)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=400, height=100, bg=CY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

# top (entering username)
username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=CY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)
username_textbox = tk.Entry(top_frame, font=FONT, bg=BG_DARK, fg=WHITE, width=20)
username_textbox.pack(side=tk.LEFT, pady=10)
username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=GREY, width=5, command=connect)
username_button.pack(side=tk.LEFT, padx=10)

# bottom (sending message)
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=BG_DARK, fg=WHITE, width=35)
message_textbox.bind("<Return>", send_message)
message_textbox.pack(side=tk.LEFT, padx=10, pady=10)
message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=GREY, width=5, command=send_message)
message_button.pack(side=tk.LEFT, padx=5)

# body (message box)
message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=BG_DARK, fg=WHITE, width=60, height=19)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)
```
> You can set up your own GUI design.

> `message_textbox.bind("<Return>", send_message)` will allow you to bind the Enter key to a tkinter window.

### Create main function for the GUI application
```python
def main():
    root.mainloop()
```
> `root.mainloop()` starts GUI execution

Put in code for starting the client and listening for incoming connections.
```python
if __name__ == '__main__':
    main()
```

## Running the Chat App
1. Open two terminal windows.
2. In the first terminal, run `python server.py` to start the server.
3. In the second terminal, run `python client.py` to start the client.
4. Repeat step 3 for additional clients.

Now you have a simple real-time chat app where clients can connect to a server and exchange messages.

## Chat App Output
<img width="614" alt="image" src="https://github.com/pitcza/event-driven-activity/assets/130303710/63a1fda5-b882-4b1d-8b5a-d54472981a56">
