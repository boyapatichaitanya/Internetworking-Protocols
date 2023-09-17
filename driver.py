import threading
import socket
import sys

name = input("Enter your name: ")
LIST_FOR_THREDS = []
#STARTING THE CONNECTION
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

#BELOW CODE IS TO SEND AND WRITE THE MESSAGES
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(name.encode('utf-8'))
            elif message == 'QUIT':
                sys.exit(2)
            else:
                print(message)
        except Exception as e:
            print('Server not responding')
            client.close()
            sys.exit(2)

def write():
    while True:
        message = '{} {}'.format(name, input(''))
        try:
            client.send(message.encode('utf-8'))
        except:
            sys.exit(0)

RECEIVED_THREAD = threading.Thread(target=receive)
RECEIVED_THREAD.start()
LIST_FOR_THREDS.append(RECEIVED_THREAD)
write_thread = threading.Thread(target=write)
write_thread.start()
LIST_FOR_THREDS.append(write_thread)
