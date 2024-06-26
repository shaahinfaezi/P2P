import threading
import socket
from models import *
import pickle 
from log import log
from reply import Reply
from request import Request


def get_key(val,dict):
   
    for key, value in dict.items():
        if value[0] == val:
            return key
 
    return "key doesn't exist"


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

players=[]
matches=[]

playerDict={}

GameInvites={}

def server_reply(client,obj):
    message = pickle.dumps(obj)
    try:
        client.send(message)
    except socket.error as e:
        str(e)
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    connected = True
    user=""
    while connected:
        try:
            rec=conn.recv(2048)
            if not rec:
                continue
            obj = pickle.loads(rec)
            if not obj:
                continue

            if obj.name=="Reply":
                if obj.msg=="Disconnected":
                    break
                elif obj.msg=="Invites":
                    value = get_key(conn,playerDict)
                    req=GameInvites.get(value)
                    server_reply(conn,req)

            if obj.name=="Login":
                if serverDb.count_documents({"Username":obj.user,"Password":obj.password})>0 and obj.user not in players:
                    msg=Reply("Success",players,matches)
                    server_reply(conn,msg)
                    players.append(obj.user)
                    playerDict[obj.user]=[conn,addr]
                    GameInvites[obj.user]=[]
                    user=obj.user

                else:
                    msg=Reply("Fail",[],[])
                    server_reply(conn,msg)
            elif obj.name=="Register":
                if serverDb.count_documents({"Firstname":obj.fn,"Lastname":obj.ln,"Username":obj.user,"Password":obj.password})>0:
                    msg=Reply("Exists",[],[])
                    server_reply(conn,msg)
                else:
                    serverDb.insert_one({"Firstname":obj.fn,"Lastname":obj.ln,"Username":obj.user,"Password":obj.password})
                    msg=Reply("Added",[],[])
                    server_reply(conn,msg)
            elif obj.name=="Request":
                opp=playerDict.get(obj.msg)
                pl=get_key(conn,playerDict)
                req=Request(pl,addr,opp[1])
                GameInvites[obj.msg].append(req)
                msg=Request("Request sent.",addr,[])
                server_reply(conn,msg)
            elif obj.name=="Accept":
                pass
            
                    




            print(f"Recieved : [{addr}] {obj.name}")
        except socket.error as e:
            str(e)
            print(f"Lost connection : {e}")
            break

    try:
        print(f"Removed {user}")
        players.remove(user)
        clients.remove(conn)
    except:
        print('Remove failed')

    print("connection closed")     
    conn.close()


def start():
    print('[SERVER STARTED]!')
    server.listen()
    while True:
        conn, addr = server.accept()
        clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()