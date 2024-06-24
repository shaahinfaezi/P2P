import random
import string
import re
from log import log
from client import *
from reply import Reply
from Register import Register


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
    connection = connect()
    send(connection,obj)
    rep=recieve(connection)
    disconnect(connection)
    if rep.msg=="Success":
        return True
    else:
        return False
    
    


def register_user(first_name, last_name, username, password):
   newAcc=Register(first_name, last_name, username, password)
   
   


def is_valid_chars(input_string):
    # Regular expression pattern to allow only English letters and standard characters
    pattern = re.compile(r'^[a-zA-Z0-9_\-]+$')
    return pattern.match(input_string) is not None

def is_valid_chars_space(input_string):
    # Regular expression pattern to allow only English letters and standard characters
    pattern = re.compile(r'^[a-zA-Z0-9_\- ]+$')
    return pattern.match(input_string) is not None
