import socket
import threading 

PORT = 5050
SERVER_IP_ADR = "192.168.8.132"
ADDR = (SERVER_IP_ADR,PORT)
FORMAT = 'utf-8'

#creating the server socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(ADDR)

#keeping track of all the active users
client_sockets = [] 

def handle_client_communication(conn, addr):
    connected = True
    while connected:
        message = conn.recv(64)
        for client in client_sockets:
            if client != conn:
                try:
                    if message != '':
                        client.send(message)
                except ConnectionError:
                    print(f"Unable to reach client with socket {client}")
                    if client in client_sockets:
                        client_sockets.remove(client)

def accepting_users():
    server_socket.listen() 
    while True:
        conn, addr = server_socket.accept() 
        client_sockets.append(conn)
        thread = threading.Thread(target=handle_client_communication,args=(conn,addr))
        thread.start() 

accepting_users() 
