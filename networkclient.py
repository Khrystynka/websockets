import pygame as pg
import sys
import time
from game import Game
from gui import Board
from network import Network
from queue import Queue

gui = Board()
player = 1
game_id = 0
q = Queue()

def send_message_from_server_to_queue(message):
    # closure onqueu
    global q
    def put_to_queue(message):
        q.put(message)
    put_to_queue(message)
    # print ("Inside network client. received message from server",message)

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


gui.game_initiating_window()
gui.display_game_status('move')

while True:
    pg.display.update()
    if not q.empty():
        message = q.get()
        print('THIS MESSAGE IS FROM SERVER TO CLIENT', message)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            print('You clicked on the board!')
            process_click()
            # if game.is_over:
            #     print('Game over with status', status, game.turn)
            #     gui.display_game_status(status, game.turn)
            #     pg.display.update()
            #     time.sleep(2)
            #     pg.time.Clock().tick(1000)
            #     game.reset()
            #     status = "next"
            #     gui.game_initiating_window()
            #     gui.display_game_status(status, game.turn)

    pg.time.Clock().tick(10)
