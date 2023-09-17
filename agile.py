#IMPORT STATEMENTS
import socket
import threading


host = '127.0.0.1' #LOCAL_HOST
port = 55555  #PORT_NUMBER

#STARTING THE SERVER FOR PROJECT EXECUTION
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#BINDING THE SERVER
server.bind((host, port))
#CHANGING THE SERVER TO LISTEN MODE
server.listen()


instructions = '\nList of commands:\n' \
               '1.$list to list all the rooms\n' \
               '2.$quit to quit\n' \
               '3.$help to list all the commands\n' \
               '4.$leave to leave the room \n' \
               '5.$join roomname to join or create the room\n' \
               '6.$switch roomname to switch room\n' \
               '7.$personal name message to send personal message'


#CREATING THE EMPTY LISTS BELOW
CLIENTS_LIST = []
NICK_NAMES_LIST = []
ROOM_DETAILS_LIST = {}
USERS_LIST = {}
USERS_IN_THE_LIST = {}

#BROADCAST
def BROADCASTING_MSG(message, ROOM_NAME):
    for client in ROOM_DETAILS_LIST[ROOM_NAME].peoples:
        msg = '['+ROOM_NAME+'] '+' '+ message
        client.send(msg.encode('utf-8'))

