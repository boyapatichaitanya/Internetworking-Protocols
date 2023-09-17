from main import *

#INIT METHOD
class User:
    def __init__(self, name):
        self.name = name
        self.ROOM_DETAILS_LIST = []
        self.thisRoom = ''


class Room:
    def __init__(self, name):
        self.peoples = []
        self.NICK_NAMES_LIST = []
        self.name = name


def LISTING_ROOM_DETAILS(nickname):
    name = USERS_LIST[nickname]
    print(len(ROOM_DETAILS_LIST))
    if len(ROOM_DETAILS_LIST) == 0:
        name.send('No ROOM_DETAILS_LIST are available to join'.encode('utf-8'))
    else:
        reply = "List of available ROOM_DETAILS_LIST: \n"
        for room in ROOM_DETAILS_LIST:
            print(ROOM_DETAILS_LIST[room].name)
            reply += ROOM_DETAILS_LIST[room].name
            print(ROOM_DETAILS_LIST[room].NICK_NAMES_LIST)

            #IF NICKNAME IS NOT IN THE ROOM_DETAILS_LIST[room].NICK_NAMES_LIST:
            for people in ROOM_DETAILS_LIST[room].NICK_NAMES_LIST:
                reply += people + '\n'
        name.send(f'{reply}'.encode('utf-8'))


def JOINING_THE_ROOM(nickname, room_name):
    name = USERS_LIST[nickname]
    user = USERS_IN_THE_LIST[nickname]
    if room_name not in ROOM_DETAILS_LIST:
        room = Room(room_name)
        ROOM_DETAILS_LIST[room_name] = room
        room.peoples.append(name)
        room.NICK_NAMES_LIST.append(nickname)

        user.thisRoom = room_name
        user.ROOM_DETAILS_LIST.append(room)
        name.send(f'{room_name} created'.encode('utf-8'))
    else:
        room = ROOM_DETAILS_LIST[room_name]
        if room_name in user.ROOM_DETAILS_LIST:
            name.send('You are already in the room'.encode('utf-8'))
        else:
            room.peoples.append(name)
            room.NICK_NAMES_LIST.append(nickname)
            user.thisRoom = room_name
            user.ROOM_DETAILS_LIST.append(room)
            BROADCASTING_MSG(f'{nickname} joined the room', room_name)
            #name.send('Joined room'.encode('utf-8'))

def SWITCHING_ROOM(nickname, roomname):
    user = USERS_IN_THE_LIST[nickname]
    name = USERS_LIST[nickname]
    room = ROOM_DETAILS_LIST[roomname]
    if roomname == user.thisRoom:
        name.send('You are already in the room'.encode('utf-8'))
    elif room not in user.ROOM_DETAILS_LIST:
        name.send('Switch not available, You are not part of the room'.encode('utf-8'))
    else:
        user.thisRoom = roomname
        name.send(f'Switched to {roomname}'.encode('utf-8'))

def EXIT_ROOM(nickname):
    user = USERS_IN_THE_LIST[nickname]
    name = USERS_LIST[nickname]
    if user.thisRoom == '':
        name.send('You are not part of any room'.encode('utf-8'))
    else:
        roomname = user.thisRoom
        room = ROOM_DETAILS_LIST[roomname]
        user.thisRoom = ''
        user.ROOM_DETAILS_LIST.remove(room)
        ROOM_DETAILS_LIST[roomname].peoples.remove(name)
        ROOM_DETAILS_LIST[roomname].NICK_NAMES_LIST.remove(nickname)
        BROADCASTING_MSG(f'{nickname} left the room', roomname)
        name.send('You left the room'.encode('utf-8'))



def SENDING_PERSONAL_MESSAGE(message):
    args = message.split(" ")
    user = args[2]
    sender = USERS_LIST[args[0]]
    if user not in USERS_LIST:
        sender.send('User not found'.encode('utf-8'))
    else:
        reciever = USERS_LIST[user]
        msg = ' '.join(args[3:])
        reciever.send(f'[personal message] {args[0]}: {msg}'.encode('utf-8'))
        sender.send(f'[personal message] {args[0]}: {msg}'.encode('utf-8'))

def CLIENT_REMOVING(nickname):
    NICK_NAMES_LIST.remove(nickname)
    client = USERS_LIST[nickname]
    user = USERS_IN_THE_LIST[nickname]
    user.thisRoom = ''
    for room in user.ROOM_DETAILS_LIST:
        print(room.name)
        room.peoples.remove(client)
        print(room.peoples)
        room.NICK_NAMES_LIST.remove(nickname)
        print(room.NICK_NAMES_LIST)
        BROADCASTING_MSG(f'{nickname} left the room', room.name)


#to handle
def handle(client):
    nick=''
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            args = message.split(" ")
            name = USERS_LIST[args[0]]
            nick = args[0]
            if '$help' in message:
                name.send(instructions.encode('utf-8'))
            elif '$list' in message:
                LISTING_ROOM_DETAILS(args[0])
            elif '$join' in message:
                JOINING_THE_ROOM(args[0], ' '.join(args[2:]))
            elif '$leave' in message:
                EXIT_ROOM(args[0])
            elif '$switch' in message:
                SWITCHING_ROOM(args[0], args[2])
            elif '$personal' in message:
                SENDING_PERSONAL_MESSAGE(message)
            elif '$quit' in message:
                CLIENT_REMOVING(args[0])
                name.send('QUIT'.encode('utf-8'))
                name.close()
            else:
                if USERS_IN_THE_LIST[args[0]].thisRoom == '':
                    name.send('You are not part of any room'.encode('utf-8'))
                else:
                    msg = ' '.join(args[1:])
                    BROADCASTING_MSG(f'{args[0]}: {msg}',USERS_IN_THE_LIST[args[0]].thisRoom)

            #BROADCASTING_MSG(message)
        except Exception as e:
            print("exception occured ", e)
            index = CLIENTS_LIST.index(client)
            CLIENTS_LIST.remove(client)
            client.close()
            '''nickname = NICK_NAMES_LIST[index]
            print(f'{nickname} left')
            user = USERS_IN_THE_LIST[nickname]'''
            '''if user.thisRoom != '':
                roomname = user.thisRoom
                user.thisRoom = ''
                #user.ROOM_DETAILS_LIST.remove(roomname)
                ROOM_DETAILS_LIST[roomname].peoples.remove(name)
                ROOM_DETAILS_LIST[roomname].NICK_NAMES_LIST.remove(nickname)
                BROADCASTING_MSG(f'{nickname} left the room', roomname)'''
            print(f'nick name is {nick}')
            if nick in NICK_NAMES_LIST:
                CLIENT_REMOVING(nick)
            if nick in NICK_NAMES_LIST:
                NICK_NAMES_LIST.remove(nick)

            #BROADCASTING_MSG(f'{nickname} left the room'.encode('utf-8'))

            break

#main
def recieve():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')
        print(client)
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        NICK_NAMES_LIST.append(nickname)
        CLIENTS_LIST.append(client)
        user = User(nickname)
        USERS_IN_THE_LIST[nickname] = user
        USERS_LIST[nickname] = client
        print(f'Nickname of the client is {nickname}')
        #BROADCASTING_MSG(f'{nickname} joined the chat'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))
        client.send(instructions.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...........')
recieve()

