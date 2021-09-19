
import pygame as pg
import sys
import time
from game import Game

game = Game()
width = 400
height = 400
board_color = (255, 255, 255)
line_color = (0, 0, 0)
cross_line_color =(255, 0, 0)
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

def cross_winner(i,direction):
    if direction =='row':
        coords = ((30,170+height/3*i),(width-30,170+height/3*i))
    elif direction =='col':
        coords = ((width/3*i+70,130),(width/3*i+70,height+100-30))
    elif i == 0:
        coords =((30,130),(width-30,height+100-30))
    else:
        coords= ((width - 30, 130), (30, height + 100 - 30))
    pg.draw.line(screen, line_color, coords[0], coords[1], 7)
    pg.display.update()


# def recalculate_game():
#     game.update_status()
#     if game.winner != None:
# #         cross_winner(game.winner_idx, game.winner_direction)
#
#
#
#     display_game_status()



def display_game_status():

    if game.winner:
            cross_winner(game.winner_idx, game.winner_direction)
            message = f"Winner is: Player {game.winner.upper()}"
    elif game.tie:
            message = "Game over!"
    else:
            message = f"Next turn: Player {game.turn.upper()}"
    font = pg.font.SysFont("comicsans", 40)

    img = font.render(message, True, (0, 0, 255))
    screen.fill((255, 0, 0), (0, 0, 500, 100))

    rect = img.get_rect(center=(width / 2, 50))
    screen.blit(img, rect)
    # pg.draw.rect(img, (0,255,0), rect, 4)
    pg.display.update()

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
def mark_board(row,col):
    print(f"Marking row{row} and col{col}with{game.turn}")
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

    if (game.turn == 'x'):
        screen.blit(x_img, (x, y))
    else:
        screen.blit(o_img, (x, y))
    pg.display.update()
def process_click(position):
    row,col = detect_square(position)
    print(f"you clicked in row {row} and col {col}")
    if  row and col and  game.is_free(row, col):
        mark_board(row, col)
        game.make_move(row,col)
        # recalculate_game()
        # game.switch_turns()
        display_game_status()

def reset_game():

    time.sleep(1)
    game.reset()
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
            if (game.is_over):
                display_game_status()
                pg.display.update()

                pg.time.Clock().tick(60)

                reset_game()
    pg.time.Clock().tick(10)
