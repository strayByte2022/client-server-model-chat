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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send_message(msg):
    message = msg.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

def enter_message():
    index = 0
    while True:
        msg = input(f'[ENTER MESSAGE {index}]: ')
        send_message(msg)
        index +=1 
enter_message()