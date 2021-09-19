
import pygame as pg
import sys
import time

turn = 'x'

winner = None
tie = None
width = 400
height = 400
board_color = (255, 255, 255)
line_color = (0, 0, 0)
board = [[None] * 3, [None] * 3, [None] * 3]
pg.init()
CLOCK = pg.time.Clock()


screen = pg.display.set_mode((width, height+100))

pg.display.set_caption("Tic Tac Toe")

# loading the images as python object

o_img = pg.image.load("letter_o.png")
x_img = pg.image.load("letter_x.png")

# resizing images
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))


def game_initiating_window():

    screen.fill(board_color)

    pg.draw.line(screen, line_color, (0, 100), (width, 100), 7)
    pg.draw.line(screen, line_color, (0, height+100), (width, height+100), 7)

    pg.draw.line(screen, line_color, (width / 3, 100), (width / 3, height+100), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 100), (width / 3 * 2, height+100), 7)

    pg.draw.line(screen, line_color, (0, 100+height / 3), (width, 100+height / 3), 7)
    pg.draw.line(screen, line_color, (0, 100+height / 3 * 2), (width, 100+height / 3 * 2), 7)
    pg.draw.line(screen, line_color, (0, 100 ), (0, 100 + height), 7)
    pg.draw.line(screen, line_color, (width, 100), (width, 100 + height ), 7)
    display_game_status()
def check_tie():
    for i in range(len(board)):
        for j in range(len(board[0])):
            if not board[i][j]:
                return False
    return True

def check_winner():
    for i in range(3):
        if board[i][0] and board[i][0] == board[i][1] ==board[i][2]:
            return (board[i][0],([30,170+height/3*i],[width-30,170+height/3*i]))
        if board[0][i] and board[0][i]==board[1][i]==board[2][i]:
            return (board[0][i],([width/3*i+70,130],[width/3*i+70,height+100-30]))
    if board[0][0] and board[0][0] ==board[1][1] ==board[2][2] :
        return (board[0][0],([30,130],[width-30,height+100-30]))
    if board[0][2] and board[0][2] ==board[1][1] ==board[2][0] :
        return (board[0][2],([width-30,130],[30,height+100-30]))
    return (None,([],[]))
def cross_winner(coords):
    pg.draw.line(screen, line_color, coords[0], coords[1], 7)
    pg.display.update()


def recalculate_game():
    global winner, tie, turn
    winner,line_coords = check_winner()
    if winner:
        cross_winner(line_coords)
    else:
        if turn == "o":
            turn = "x"
        else:
            turn = 'o'
        tie = check_tie()

    display_game_status()



def display_game_status():
    global winner, tie, turn
    if tie:
        message = "Game over!"
    elif winner:
            message = f"Winner is Player {winner}"
    else:
            message = f"Next turn player {turn}"
    font = pg.font.SysFont("comicsans", 40)

    img = font.render(message, True, (0, 0, 255))
    screen.fill((255, 0, 0), (0, 0, 500, 100))

    rect = img.get_rect(center=(width / 2, 50))
    screen.blit(img, rect)
    # pg.draw.rect(img, (0,255,0), rect, 4)

def detect_square(pos):
    x= pos[0]
    y= pos[1]
    if x < width/3:
        col =1
    elif x < width/3*2:
        col=2
    else:
        col=3
    if y < 100:
        row = None
    elif y <100+height/3:
        row = 1
    elif y < 100+height/3*2:
        row = 2
    else:
        row =3
    return (row, col)
def mark_board(row,col,turn):
    print(f"Marking row{row} and col{col}with{turn}")
    global board
    margin_x = 30
    margin_y =130
    if col == 1:
        x = margin_x
    if col == 2:
        x = width / 3 + margin_x
    if col == 3:
        x = width / 3 * 2 + margin_x

    if row == 1:
        y = margin_y

    if row == 2:
        y = height / 3 + margin_y

    if row == 3:
        y = height / 3 * 2 + margin_y
    board[row - 1][col - 1] = turn

    if (turn == 'x'):
        screen.blit(x_img, (x, y))

    else:
        screen.blit(o_img, (x, y))
    pg.display.update()
def process_click(position):
    global turn
    row,col = detect_square(position)
    print(f"you clicked in row {row} and col {col}")
    if  row and col and not board[row-1][col-1]:
        mark_board(row, col, turn)
        recalculate_game()

def reset_game():
    global board, winner, turn, tie
    time.sleep(3)
    turn = 'x'
    tie = False
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]
    game_initiating_window()



game_initiating_window()

while (True):

    # display_game_status()
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            print('Clicked!')
            process_click(pos)
            if (winner or tie):
                display_game_status()
                pg.display.update()

                pg.time.Clock().tick(60)

                reset_game()
    pg.time.Clock().tick(10)
