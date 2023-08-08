# client.py
import socket
import threading
import sys
HEADER = 1024
 # netstat -ano -> choose listening ports

host_name = socket.gethostname() # automatically get the addr that the host run on
SERVER = socket.gethostbyname(host_name) 
PORT = 50446
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER,50445)) # in the case of 2 diff hosts, find address by ipconfig, be sure to be on the same port

def print_avail_message():
        while True: 
       
            message_length = client.recv(HEADER).decode(FORMAT)
            if message_length:
                message_length = int(message_length)
                message = client.recv(message_length).decode(FORMAT)
                if message == '!bye':
                    print('Disconnect from server') 
                    break
                print(f'[SERVER]: {message}')
       
def send_message(msg):
    message = msg.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

def enter_message():
    receive_thread = threading.Thread(target=print_avail_message)
    receive_thread.start()
       
    
    while True:
        msg = input('>>')
    
        send_message(msg)
        if msg == '!bye':
            break

def enter_username():
    while True:
        username = input('Enter username: ')
        if ' ' not in username:
            send_message(username)
            break
        else: 
            print('Username cannot contain white space. Please enter again')


if __name__ == '__main__':
    enter_username()
    enter_message()