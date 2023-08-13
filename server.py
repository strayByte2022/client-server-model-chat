# server.py
import socket
import threading

HEADER = 1024 # Maximum bytes for message's length
# Set server socket at the address that the host run on
SERVER = socket.gethostbyname(socket.gethostname())
# Can use netstat -a to find used ports
PORT = 50445
ADDR = (SERVER, PORT)
FORMAT = 'utf-8' # Standard format for the message transmitted

# bind address to socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet socket using TCP connection
server.bind(ADDR) # Bind the socket to the designated address

blue_lock = threading.Lock() # Mutex lock for accessing the clients' list

# list of clients
clients = {}
def get_online_users():
    '''Return a list of online clients by their nickname'''
    with blue_lock:
        return [clients[addr]['username'] for addr in clients]
    

def send_private_message(sender_address, recipient_address,message):
    '''Send a private message to a designated address
    '''
    with blue_lock:
        # Iterate through the clients' list, find the designated client
        for address, client_info in clients.items():
            if client_info['username'] == recipient_address:
                recipient_connection = client_info['connection']
                private_message = f'[PRIVATE MESSAGE from {clients[sender_address]["username"]}]: {message}'
                send_message_to_clients(recipient_connection,private_message)
                break
    pass            

def handle_client(connection, address):
    '''General handle client function. Parameters include:
    
        connection: TCP connection from socket to the client

        address: client's address'''
    print(f'[NEW CONNECTION] {address} connected.')
    
  
    with blue_lock:
        # Handle client's nickname and store corresponding connection into clients dict
        username_length = connection.recv(HEADER).decode(FORMAT)
        username_length = int(username_length)
        username = connection.recv(username_length).decode(FORMAT)
        clients[address] = {'connection':connection,'username':username}
    
    # Notify to other client's about new connection
    connected_noti = f'[NEW CONNECTION] User {username} connected.'
    broadcast_message(connected_noti,address)

    connected = True
    while connected:
        # Loop for handle messages from clients
        message_length = connection.recv(HEADER).decode(FORMAT) # convert bytes format -> string 
        if message_length:
            # Received a message's length (message_length != 0)
            message_length = int(message_length)
            message = connection.recv(message_length).decode(FORMAT)
           
            if message == '!bye':
                # Terminate message from client
                connected = False
                disconnection_noti = f'Host on {address} has disconnected from server!'
                broadcast_message(disconnection_noti,address)
            elif message == '!online':
                # Request list of online client
                online_users =", ".join(get_online_users())
                send_message_to_clients(connection,f'Online users ({threading.active_count()-1}): {online_users}')
            elif message.startswith('!private '):
                # Private message
                recipient, private_message = message[len('!private '):].split(' ',1)
                send_private_message(address,recipient,private_message)
            else:
                # Broadcast message
                broadcast_message(f'[{clients[address]["username"]}] said: {message}', address)
            print(f'[{address}, username = {clients[address]["username"]} ] said: {message}') # on server side 
        
    # Remove the disconnected client
    with blue_lock:
        del clients[address]
    print(f'[DISCONNECTED] {address} disconnected')
    connection.close()

def broadcast_message(msg,client_address):
    '''Broadcast function: send message to all online clients'''
    with blue_lock: 
        for address,connection in clients.items():
            if address != client_address:   # avoid sending to sender
                send_message_to_clients(connection['connection'],msg)


def send_message_to_clients(connection,message):
    '''One-to-one message sending function'''
    message = message.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length+=b' '*(HEADER-len(send_length))
    connection.send(send_length)
    connection.send(message)


def start():
    '''Launching function for server'''
    server.listen() # Begin listening
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        connection,address = server.accept() # connection = socket objects
        # Create new thread for handling newly connected client
        thread = threading.Thread(target=handle_client,args=(connection,address))
        thread.start()
        print(f'\n[ACTIVE CONNECTIONS] {threading.active_count()-1}')


if __name__ == '__main__':
    print(f'[STARTING] server is starting on port {PORT}')
    start()