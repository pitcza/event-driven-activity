import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

# styles for GUI
CY = '#00ABB3'
BG_DARK = '#3C4048'
GREY = '#B2B2B2'
WHITE = "white"
FONT = ("Tahoma", 13)
BUTTON_FONT = ("Tahoma", 11)
SMALL_FONT = ("Tahoma", 10)

# configuration
HOST = '127.0.0.1'
PORT = 1100

# creating the socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# to send an add-user message to the server
def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

# connect clients to the server
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

# get client's messages
def send_message(event=None):
    message = message_textbox.get()
    client.sendall(message.encode())
    message_textbox.delete(0, len(message))
    
# receive client's messages to the server
def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]
            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

# GUI setup
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

# MAIN FUNCTION
def main():
    root.mainloop()
    
if __name__ == '__main__':
    main()
