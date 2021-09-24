import pygame as pg
import sys
import time
from game import Game
from gui import Board
from network import Network
from queue import Queue

gui = Board()
player = None
game_id = None
status = None
q = Queue()

def send_message_from_server_to_queue(message):
    # closure onqueu
    global q
    def put_to_queue(message):
        q.put(message)
    put_to_queue(message)

n = Network(send_message_from_server_to_queue)
n.connect()

def process_click():
    global status
    pos = pg.mouse.get_pos()
    row, col = gui.detect_square(pos)
    if row == None:
        return
    n.send_task(f'{row},{col},{player},{game_id}')
    # if game.is_free(row, col):
    #     gui.mark_board(row, col, game.turn)
    #     game.make_move(row, col)
    #     if game.winner:
    #         gui.cross_winner(game.winner_idx, game.winner_direction)
    #         status = 'win'
    #         game.turn = game.winner
    #     elif game.tie:
    #         status = 'tie'
    #     gui.display_game_status(status, game.turn)
    #     pg.display.update()
def update_status(message):
    global player, game_id, status
    params = message.split(',')
    print('Message params',params)
    event=params[0]
    if event == 'init':
        print('Nothing on board, we initiating')
        player = int(params[1])
        game_id = int(params[2])
        if player != 1:
            status = 'opponent'
        else:
            status = 'move'
        gui.game_initiating_window()
    elif event == 'move':
        row= int(params[1])
        col= int(params[2])
        goes_player = int(params[3])
        sent_status = params[4]
        gui.mark_board(row,col,goes_player)
        status = 'move'
        if sent_status == 'win':
            gui.cross_winner(int(params[5]),params[6])
            if not player == goes_player:
                status = 'lost'
            else:
                status='win'
        elif sent_status =='tie':
            status = 'tie'
        elif player == goes_player:
            status = 'opponent'
    elif event == "not ready":
        status ='not ready'
    gui.display_game_status(status)

while True:
    pg.display.update()
    if not q.empty():
        message = q.get()
        update_status(message)
        pg.display.update()
        print('THIS MESSAGE IS FROM SERVER TO CLIENT', message)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            print('You clicked on the board!')
            process_click()


    pg.time.Clock().tick(10)
