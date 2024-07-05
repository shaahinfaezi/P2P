import pygame
import math
from p2p import *
import threading

pygame.init()

# Screen
WIDTH = 300
ROWS = 3
global win
win = None


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("ClientSide/images/x.png"), (80, 80))
O_IMAGE = pygame.transform.scale(pygame.image.load("ClientSide/images/o.png"), (80, 80))

# Fonts
END_FONT = pygame.font.SysFont('arial', 40)


global Client
global Role
global Turn
global moveTurn
global run
moveTurn=1

def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)


def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y, "", True)

    return game_array

class Move():
    def __init__(self,x,y,xo,i,j):
        self.name="Move"
        self.x=x
        self.y=y
        self.xo=xo
        self.i=i
        self.j=j


def click(game_array):
    global x_turn, o_turn, images

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            global moveTurn
            # If it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                if moveTurn==1:  # If it's X's turn
                    moveTurn=2
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = (x, y, 'x', False)
                    move=Move(x,y,"x",i,j)
                    if Role=="client":
                        clientSend(move)
                    else:
                        server_reply(Client,move)
                    return

                elif moveTurn==2:  # If it's O's turn
                    moveTurn=1
                    images.append((x, y, O_IMAGE))
                    x_turn = True
                    o_turn = False
                    game_array[i][j] = (x, y, 'o', False)
                    move=Move(x,y,"o",i,j)
                    if Role=="client":
                        clientSend(move)
                    else:
                        server_reply(Client,move)
                    return 


# Checking if someone has won
def has_won(game_array):
    # Checking rows
    for row in range(len(game_array)):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            display_message(game_array[row][0][2].upper() + " has won!")
            return True

    # Checking columns
    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            display_message(game_array[0][col][2].upper() + " has won!")
            return True

    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won!")
        return True

    # Checking reverse diagonal
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        display_message(game_array[0][2][2].upper() + " has won!")
        return True

    return False


def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True


def display_message(content):
    win.fill(BLACK)
    end_text = END_FONT.render(content, 1, "#669BBC")
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(1000)


def render():
    win.fill(BLACK)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()


def handle_peer(role,client):
    global run
    global Turn
    global obj
    while run:
            try:
                if role=="client":
                    obj=clientRecieve()
                else:
                    rec=client.recv(2048)
                    if not rec:
                        continue
                    obj = pickle.loads(rec)
                    if not obj:
                        continue
            except socket.error as e:
                print(e)

def TicTacToe(turn,role,client=None):
    global Client
    Client=client
    global Role
    Role=role
    global Turn
    Turn=turn
    global win

    global moveTurn

    win=pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption(f"TTT Turn : {turn} Role : {role} ")
    global x_turn, o_turn, images, draw

    images = []
    draw = False

    global run
    run = True

    x_turn = True
    o_turn = False

    game_array = initialize_grid()

    global obj
    obj=None

    thread = threading.Thread(target=handle_peer, args=(role,client))
    thread.start()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if moveTurn==turn:
                    click(game_array)

        

        if moveTurn!=Turn:
                if obj is not None:
                    
                    if obj.name=="Move":
                        if obj.xo=="x":
                            images.append((obj.x, obj.y, X_IMAGE))
                            moveTurn=2
                            # x_turn = False
                            # o_turn = True
                            game_array[obj.i][obj.j] = (obj.x, obj.y, 'x', False)
                        elif obj.xo=="o":
                            moveTurn=1
                            images.append((obj.x, obj.y,O_IMAGE))
                            # x_turn = True
                            # o_turn = False
                            game_array[obj.i][obj.j] = (obj.x, obj.y, 'o', False)
                        obj=None

        render()

        if has_won(game_array) or has_drawn(game_array):
            run = False
            exit()

