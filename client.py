import socket
import threading
import time
HEADER = 64 
 # netstat -ano -> choose listening ports

host_name = socket.gethostname() # automatically get the addr that the host run on
SERVER = socket.gethostbyname(host_name) 
PORT = 50446
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.100.4',50445)) # in the case of 2 diff hosts, find address by ipconfig, be sure to be on the same port

def send_message(msg):
    message = msg.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

def enter_message():
    
    while True:
        msg = input(f'[ENTER MESSAGE]: ')
        if msg == '!disconnect':
            send_message(msg)
            break
        send_message(msg)
        
        

if __name__ == '__main__':

    enter_message()