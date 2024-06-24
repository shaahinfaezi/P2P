import threading
import socket
from models import *
import pickle 
from log import log
from reply import Reply


PORT = 5555
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((SERVER, PORT))
except socket.error as e:
    str(e)

clients = set()
clients_lock = threading.Lock()



def server_reply(client,obj):
    message = pickle.dumps(obj)
    client.send(message)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    try:
        connected = True
        while connected:
            rec=conn.recv(2048)
            if not rec:
                break
            obj = pickle.loads(rec)
            if not obj:
                break

                # if msg == DISCONNECT_MESSAGE:
                #     connected = False
            if obj.name=="Login":
                if serverDb.count_documents({"Username":obj.user,"Password":obj.password})>0:
                    msg=Reply("Success")
                    server_reply(conn,msg)
                else:
                    msg=Reply("Fail")
                    server_reply(conn,msg)




            print(f"Recieved : [{addr}] {obj.name}")
    

    finally:
        with clients_lock:
            clients.remove(conn)

        conn.close()


def start():
    print('[SERVER STARTED]!')
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()