import pygame as pg
import sys
import time
from game import Game
from gui import Board
from network import Network
from queue import Queue
import pickle

gui = Board()
player = None
game_id = None
status = None
q = Queue()
board = None

def reset_board():
    global board
    board = [[None] * 3, [None] * 3, [None] * 3]
    # gui.game_initiating_window()
def send_message_from_server_to_queue(message):
    # closure on queue
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
    print ('clicked on', row, col, board[row-1][col-1])
    if row is None or (row and board[row-1][col-1]):
        return
    board[row-1][col-1] = 'marked'
    n.send_task(f'{row},{col},{player},{game_id}')


def update_status(message):
    global player, game_id, status,q, board
    response = pickle.loads(message)
    print ('Client works on', response)
    game_status = None
    if response['action'] == 'init':
        print('Nothing on board, we initiating')
        player = int(response['player'])
        game_id = int(response['game_id'])
        board = response['board']
        print("The board",board)
        print('init', 'player', player, 'game_id', game_id)
        if player != 1:
            status = 'opponent'
        else:
            status = 'move'
        gui.game_initiating_window()
    elif response['action'] == 'move':
        row = int(response['row'])
        col = int(response['col'])
        goes_player = int(response['player'])
        game_status = response['status']
        board = response['board']

        gui.mark_board(row, col, goes_player)
        status = 'move'
        if game_status == 'win':
            gui.cross_winner(response['winner_id'], response['winner_dir'])
            if not player == goes_player:
                status = 'lost'
            else:
                status = 'win'
        elif game_status == 'tie':
            status = 'tie'
        elif player == goes_player:
            status = 'opponent'
    elif response['action'] == "not ready":
        status = 'not ready'
        gui.game_initiating_window()
    gui.display_game_status(status)

    if game_status == "win" or game_status == 'tie':
        print('remaining tasks',n.tasks)
        # while not n.tasks.empty():
        #     task = n.tasks.get()
        #     task.cancel()
        # print('remaining tasks after closing',n.tasks)

        time.sleep(5)
        gui.game_initiating_window()
        if player != 1:
            status = 'opponent'
        else:
            status = 'move'

        # gui.game_initiating_window()
        gui.display_game_status(status)
        reset_board()



while True:
    pg.display.update()
    if not q.empty():
        message = q.get()
        update_status(message)
        pg.display.update()
        q.task_done()
        # print('THIS MESSAGE IS FROM SERVER TO CLIENT', message)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            process_click()

    pg.time.Clock().tick(60)
