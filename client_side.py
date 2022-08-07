import socket
import threading 
from tkinter import *

PORT = 5050
SERVER_IP_ADR = "192.168.8.132"
ADDR = (SERVER_IP_ADR,PORT)
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(ADDR)

def send():
    user_message = e.get() 
    e.delete(0, END)
    if user_message != '':
        text_widget.insert(END, "\n" + f"{username}: {user_message}")
        client_socket.send(f"{username}: {user_message}".encode(FORMAT))

def recieving_messages():
    while True:
        message = client_socket.recv(24)
        message = message.decode(FORMAT)
        text_widget.insert(END, "\n" + message)

window = Tk() 
window.title("Chat app!")
window.resizable(False, False)

text_widget = Text(window, bg = "black", fg = "white", font = "Helvetica 14", width = 60)
text_widget.grid(row = 1, column = 0, columnspan = 2)

scrollbar = Scrollbar(text_widget,cursor="arrow")
scrollbar.place(relheight = 1, relx = 0.974)

scrollbar.config(command=text_widget.yview)

e = Entry(window, bg = "red", fg = "#EAECEE", font = "Helvetica 14", width = 55)
e.grid(row = 2, column = 0)

send = Button(window, text = "Send", font = "Helvetica 13 bold", bg = "#ABB2B9",
              command = send).grid(row = 2, column = 1)

window.withdraw() 

top_window = Toplevel() 
top_window.config(bg="gray")
top_window.title("Waiting room...")
top_window.geometry("800x500")

a_label = Label(top_window, text = "Welcome to the chat room!", font = ("constantia",16), bg="gray")
a_label.place(relx = 0.5, rely = 0.5, anchor = CENTER) 

another_label = Label(top_window, text = "Username:", font = ("constantia",14), bg="gray")
another_label.place(relx = 0.35, rely = 0.6, anchor = CENTER) 

username_entry = Entry(top_window)
username_entry.place(relx = 0.5, rely = 0.6, anchor = CENTER) 

def submit():
    global username
    username = username_entry.get() 
    top_window.destroy()
    window.deiconify() 
    text_widget.insert(END, "\n" + f"{username} connected.")
    client_socket.send(f"{username} connected.".encode(FORMAT))
    thread1 = threading.Thread(target = recieving_messages)
    thread1.start()

submit_button = Button(top_window, text="Submit", command=submit, bg="red")
submit_button.place(relx=0.65, rely=0.6, anchor=CENTER) 

top_window.mainloop()




