# client.py
import socket
import threading
import sys

HEADER = 1024 # Maximum bytes for message's length
# Set server socket at the address that the host run on
SERVER = socket.gethostbyname(socket.gethostname())
# Can use netstat -a to find used ports
PORT = 50445
ADDR = (SERVER, PORT)
FORMAT = 'utf-8' # Standard format for the message transmitted

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet socket using TCP connection
# in the case of 2 different hosts, find the address by ipconfig, be sure to be on the same port
client.connect((SERVER, 50445))  

# A synchronization object that signals the occurrence of an event or the completion of an operation
stop_receive_thread = threading.Event()


def print_avail_message():
    '''Message receiving function; listening to the server, 
    print if receive message, exit if '!bye' is entered from the user
    '''
    while not stop_receive_thread.is_set():
        # Listening to the server
        message_length = client.recv(HEADER).decode(FORMAT)
        
        if message_length:
            # Received a message's length (message_length != 0)
            message_length = int(message_length)
            # Receive the message
            message = client.recv(message_length).decode(FORMAT)

            print(f'[SERVER]: {message}')
    client.close()


def send_message(msg):
    '''Message sending function; send a message's length (byte-like object)
    and then the utf-8-encoded message to server
    '''
    message = msg.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def enter_message():
    '''Handle function for client, process input message from the user.
        Available message's types:
            Broadcast: any message that does not contain special keywords
            
            Private message: !private <username> <message>
            
            Terminate: !bye'''
    # Thread for message's listening from the server
    receive_thread = threading.Thread(target=print_avail_message)
    receive_thread.start()
    # Loop for inputting message from the user's terminal
    while True:
        msg = input('>>')
        if msg.startswith('!private '):
            recipient_username, private_msg = msg[len('!private '):].split(' ', 1)
            send_message(f'!private {recipient_username} {private_msg}')
        else:
            send_message(msg)
        if msg == '!bye':
            stop_receive_thread.set()
            break

    receive_thread.join()
    client.close()


def enter_username():
    '''Function for send first message to the server, declaring the client's name,
    retry if the name already exist.'''
    while True:
        username = input('Enter username: ')
        if ' ' not in username:
            send_message(username)
            break
        else:
            print('Username cannot contain white space. Please enter again')

# Start the client
if __name__ == '__main__':
    enter_username()
    enter_message()
    sys.exit(0)
