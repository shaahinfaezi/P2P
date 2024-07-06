from Login.app import MainApp
from client import *
from reply import Reply
from p2p import *
import threading
from TTT import TicTacToe
import random
from datetime import datetime


import atexit
global first
first=True

global app
app=None

def handle_client():
    try:
        conn, addr = server.accept()
        if conn!=None:
            random.seed(datetime.now().timestamp())
            turn=random.randint(1,2)
            if turn==1:
                re=Reply("x",[],[])
                server_reply(conn,re)
                TicTacToe(2,"server",None,conn)
            else:
                re=Reply("o",[],[])
                server_reply(conn,re)
                TicTacToe(1,"server",None,conn)

            

            return
            
            
    except socket.error as e:
        print(e)




if __name__ == "__main__":
    connect()
    app = MainApp()
    while True:
        if readyCheck():
            if first==True:
                thread = threading.Thread(target=handle_client)
                thread.start()
                first=False
        app.update_idletasks()
        app.update()



@atexit.register
def goodbye():
    rep=Reply("Disconnected",[],[])
    send(client,rep)