import socket
import threading

# server configuration
HOST = '127.0.0.1'
PORT = 1100
LISTENER_LIMIT = 4
clients = [] # list to store connected clients

# listen for upcoming messages from a client
def broadcast(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f"The message send from client {username} is empty")

# send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# send new messages to all the clients that are currently connected to the server
def send_messages_to_all(message):
    for user in clients:
        send_message_to_client(user[1], message)

# handle client
def client_handler(client):
    # server will listen for connected client and includes the username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} joined the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=broadcast, args=(client, username, )).start()

# MAIN FUNCTION
def main():
    # creating the socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT)) # bind the socket to a specific address and port
        print(f"Server listening on {HOST} : {PORT}")
    except:
        print(f"Unable to bind host {HOST} and port {PORT}")

    # set server limit
    server.listen(LISTENER_LIMIT)

    # keep listening to client connections
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()