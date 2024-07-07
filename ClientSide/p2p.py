import socket
import time
import pickle

##client
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

client_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def clientConnect(addr):
    try:
        client_.connect(addr)
    except socket.error as e:
        str(e)
        print(f"Couldnt connect : {e}")






def clientSend(obj):
    message = pickle.dumps(obj)
    client_.send(message)

def clientRecieve():
    obj=pickle.loads(client_.recv(2048))
    if obj==None:
        return
    return obj

##server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



readyToAccept=False

def serverBind(addr):

    global readyToAccept
    readyToAccept=True
    try:
        server.bind(addr)
        server.listen(2)
        print(f"Socket binded to the address : {addr}")

    except socket.error as e:
        str(e)

def readyCheck():
    global readyToAccept
    return readyToAccept


def server_reply(client,obj):
    message = pickle.dumps(obj)
    try:
        client.send(message)
    except socket.error as e:
        str(e)
def serverDisconnect():
    server.close()

