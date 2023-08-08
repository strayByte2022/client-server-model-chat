#
import socket
import threading

HEADER = 1024
# netstat -ano -> choose listening ports
# automatically get the addr that the host run on
host_name = socket.gethostname()
SERVER = socket.gethostbyname(host_name) 
PORT = 50445
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

# bind address to socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #streaming data through ipv4
server.bind(ADDR) 
# for mutex lock
blue_lock = threading.Lock()

# list of clients
clients = {}
def get_online_users():
    with blue_lock:
        return [clients[addr]['username'] for addr in clients]
def handle_client(connection, address):
    print(f'[NEW CONNECTION] {address} connected.')
    
  
    with blue_lock:
        username_length = connection.recv(HEADER).decode(FORMAT)
        username_length = int(username_length)
        username = connection.recv(username_length).decode(FORMAT)
        clients[address] = {'connection':connection,'username':username}
    
    connected_noti = f'[NEW CONNECTION] User {username} connected.'
    broadcast_message(connected_noti,address)

    connected = True
    while connected:

        message_length = connection.recv(HEADER).decode(FORMAT) # convert bytes format -> string 
        if message_length:
            message_length = int(message_length)
            message = connection.recv(message_length).decode(FORMAT)
           

            if message == '!bye':
                connected = False
                disconnection_noti = f'Host on {address} has disconnected from server!'
                broadcast_message(disconnection_noti,address)
            elif message == '!online':
                online_users =", ".join(get_online_users())
                send_message_to_clients(connection,f'Online users ({threading.active_count()-1}): {online_users}')
            else:
                broadcast_message(f'[{clients[address]["username"]}] said: {message}', address)
            print(f'[{address}, username = {clients[address]["username"]} ] said: {message}') # on server side 
        

    with blue_lock:
        del clients[address]
        
    print(f'[DISCONNECTED] {address} disconnected')
    connection.close()

def broadcast_message(msg,client_address): 
    with blue_lock: 
        for address,connection in clients.items():
            if address != client_address:
                send_message_to_clients(connection['connection'],msg)


def send_message_to_clients(connection,message):
    message = message.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length+=b' '*(HEADER-len(send_length))
    connection.send(send_length)
    connection.send(message)


def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        connection,address = server.accept() # connection = socket objects
        thread = threading.Thread(target=handle_client,args=(connection,address))
        thread.start()
        print(f'\n[ACTIVE CONNECTIONS] {threading.active_count()-1}')


if __name__ == '__main__':
    print(f'[STARTING] server is starting on port {PORT}')
    start()