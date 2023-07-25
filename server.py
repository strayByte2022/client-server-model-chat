import socket
import threading
import time

HEADER = 64 
PORT = 3472 # netstat -ano -> choose listening ports
# automatically get the addr that the host run on
host_name = socket.gethostname()
SERVER = socket.gethostbyname(host_name) 
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

# bind address to socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #streaming data through ipv4
server.bind(ADDR)


def handle_client(connection, address):
    print(f'[NEW CONNECTION] {address} connected.')
    connected = True
    while connected:
        message_length = connection.recv(HEADER).decode(FORMAT) # convert bytes format -> string 
        if message_length:
            message_length = int(message_length)

            message = connection.recv(message_length).decode(FORMAT)
            if message == '!disconnect':
                connected = False
        
            print(f'[{address}] said: {message}')

    connection.close()

def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        connection,address = server.accept()
        thread = threading.Thread(target=handle_client,args=(connection,address))
        thread.start()
        print(f'\n[ACTIVE CONNECTIONS] {threading.active_count()-1}')

print('[STARTING] server is starting')
start()