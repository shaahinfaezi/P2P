import random
import string
import re
from log import log
from client import *
from reply import Reply
from Register import Register
from request import Request
from p2p import *
from TTT import TicTacToe
import threading


invites=[]

def toggle_password(p_block, show_password_var):
    if show_password_var.get():
        p_block.configure(show="")
    else:
        p_block.configure(show="*")

def generate_temporary_password(length=8):
    # Generate a random temporary password
    characters = string.ascii_letters + string.digits
    temporary_password = ''.join(random.choice(characters) for letters in range(length))
    return temporary_password

def check_login(username, password):
    obj=log(username, password)
    connection = client
    try:
        send(connection,obj)
    except socket.error as e:
        str(e)
    try:
        rep=recieve(connection)
    except socket.error as e:
        str(e)
    if rep.msg=="Success":
        return True,rep.players,rep.matches
    else:
        return False,[],[]
    
def findInv(user):
    for item in invites:
        if item.msg==user:
            return item


def accept(user):
    req=findInv(user)
    pack=Request("Accept",req.source,req.dest)
    pack.name="Accept"
    try:
        send(client,pack)
    except socket.error as e:
        str(e)
    print(req.source)
    clientConnect(req.source)
    re=clientRecieve()
    turn=1
    if re.msg=="x":
        turn=1
    elif re.msg=="o":
        turn=2

    TicTacToe(turn)



    

    

def register_user(first_name, last_name, username, password):
    newAcc=Register(first_name, last_name, username, password)
    connection = client
    try:
        send(connection,newAcc)
    except socket.error as e:
        str(e)
    try:
        rep=recieve(connection)
    except socket.error as e:
        str(e)
    if rep.msg=="Added":
        return True
    else:
        return False
    
    
def request(user):
    if user==None:
        print("select an item!")
        return
    rep=Request(user,None,None)
    try:
        send(client,rep)
    except socket.error as e:
        str(e)
    try:
        rep=recieve(client)
        print(rep.msg)
        serverBind(rep.source)
    except socket.error as e:
        str(e)
    
def getInvites():
    rep=Reply("Invites",None,None)
    try:
        send(client,rep)
    except socket.error as e:
        str(e)
    try:
        global invites
        invites=recieve(client)
        return invites
    except socket.error as e:
        str(e)

   


def is_valid_chars(input_string):
    # Regular expression pattern to allow only English letters and standard characters
    pattern = re.compile(r'^[a-zA-Z0-9_\-]+$')
    return pattern.match(input_string) is not None

def is_valid_chars_space(input_string):
    # Regular expression pattern to allow only English letters and standard characters
    pattern = re.compile(r'^[a-zA-Z0-9_\- ]+$')
    return pattern.match(input_string) is not None
