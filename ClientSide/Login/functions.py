import random
import string
import re
from log import log
from client import *
from reply import Reply
from Register import Register
from request import Request
from p2p import *
from TTT import TicTacToe,TicTacToe_Viewer
import threading
from PIL import ImageTk, Image
from tkinter import messagebox
from CTkListbox import *
import tkinter
import customtkinter
import bcrypt
from Matches import Match

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

def watch(match,matches):
    matchid=None
    p1=None
    p2=None
    for item in matches:
        if f"{item.p1} Vs {item.p2}"==match:
            matchid=pickle.loads(item.matchId)
            p1=item.p1
            p2=item.p2
            print(matchid)
            break
    mat=Match(p1,p2,None,matchid)
    mat.name="Watch"
    try:
        send(client,mat)
    except socket.error as e:
        str(e)
    try:
        rep=recieve(client)
        if rep.msg=="Grid":
            TicTacToe_Viewer(p1,p2,matchid,client,rep.players)
        else:
            print(rep.msg)
    except socket.error as e:
        str(e)



def accept(user,listbox:CTkListbox):
    if user is None:
        print("Select first!")
        return
    req=findInv(user)
  

    listbox.delete(listbox.curselection())
    pack=Request("Accept",req.source,req.dest)
    pack.name="Accept"
    try:
        send(client,pack)
    except socket.error as e:
        str(e)
    try:
        rep=recieve(client)
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

    TicTacToe(turn,"client",rep.players,None)
    

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


    

    

def register_user(first_name, last_name, username, password):
    hashed_password=hash_password(password)
    newAcc=Register(first_name, last_name, username, hashed_password)
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
