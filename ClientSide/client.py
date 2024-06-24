import socket
import time
import pickle


PORT = 5555
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"



def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def disconnect(client):
    client.close()



def send(client, obj):
    message = pickle.dumps(obj)
    client.send(message)

def recieve(client):
    obj=pickle.loads(client.recv(2048))
    if obj==None:
        return
    return obj

