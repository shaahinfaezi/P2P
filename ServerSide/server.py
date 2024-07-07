import threading
import socket
from models import *
import pickle 
from log import log
from reply import Reply
from request import Request
import bcrypt
from uuid import uuid4
from Matches import Match

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def get_key(val,dict,item):
   
    for key, value in dict.items():
        if value[item] == val:
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

def initialize_grid():
    dis_to_cen = 300 // 3 // 2

    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            game_array[i][j] = (x, y, "", True)

    return game_array

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
                    value = get_key(conn,playerDict,0)
                    req=GameInvites.get(value)
                    server_reply(conn,req)
                elif obj.msg=="Finish":
                    matchDb.update_one({"matchId":pickle.dumps(obj.players)},{"$set": { "state": "off" }})

            if obj.name=="Login":
                if serverDb.count_documents({"Username":obj.user})>0 and obj.user not in players:
                    if check_password(obj.password,serverDb.find_one({"Username":obj.user})["Password"]):
                        matches=matchDb.find({"state":"on"})
                        m=[]
                        for item in matches:
                            m.append(Match(item["p1"],item["p2"],None,item["matchId"]))
                        msg=Reply("Success",players,m)
                        server_reply(conn,msg)
                        players.append(obj.user)
                        playerDict[obj.user]=[conn,addr]
                        GameInvites[obj.user]=[]
                        user=obj.user

                else:
                    msg=Reply("Fail",[],[])
                    server_reply(conn,msg)
            elif obj.name=="Register":
                if serverDb.count_documents({"Firstname":obj.fn,"Lastname":obj.ln,"Username":obj.user,"Password":obj.password})>0 or serverDb.count_documents({"Username":obj.user})>0:
                        msg=Reply("Exists",[],[])
                        server_reply(conn,msg)
                else:
                    serverDb.insert_one({"Firstname":obj.fn,"Lastname":obj.ln,"Username":obj.user,"Password":obj.password})
                    msg=Reply("Added",[],[])
                    server_reply(conn,msg)
            elif obj.name=="Request":
                opp=playerDict.get(obj.msg)
                pl=get_key(conn,playerDict,0)
                req=Request(pl,addr,opp[1])
                GameInvites[obj.msg].append(req)
                msg=Request("Request sent.",addr,[])
                server_reply(conn,msg)
            elif obj.name=="Accept":
                p1=get_key(obj.source,playerDict,1)
                p2=get_key(obj.dest,playerDict,1)
                
                grid=initialize_grid()
                matchId=uuid4()
                matchDb.insert_one({"p1":p1,"p2":p2,"grid":pickle.dumps(grid),"matchId":pickle.dumps(matchId),"state":"on"})
                rep=Reply("Match Started!",matchId,[])
                server_reply(conn,rep)
            elif obj.name=="Watch":
                mat=matchDb.find_one({"p1":obj.p1,"p2":obj.p2})
                if pickle.loads(mat["matchId"])==obj.matchId:
                    if mat["state"]=="off":
                        rep=Reply("Match has ended!",[],[])
                        server_reply(conn,rep)
                    else:
                        Grid=pickle.loads(mat["grid"])
                        rep=Reply("Grid",Grid,[])
                        server_reply(conn,rep)
            elif obj.name=="Grid":
                matchDb.update_one({"matchId":pickle.dumps(obj.players)},{"$set": { "grid": pickle.dumps(obj.msg) }})
                #add reply
                
            
            
                    




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