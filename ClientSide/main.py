from Login.app import MainApp
from client import *
from reply import Reply

import atexit

if __name__ == "__main__":
    connect()
    app = MainApp()
    app.mainloop()


@atexit.register
def goodbye():
    rep=Reply("Disconnected",[],[])
    send(client,rep)