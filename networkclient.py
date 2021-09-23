# import time
# from  network import Network
# n=Network()
# n.connect()
#
# while True:
#     print('Is it goint to be here?')
#     n.send(f"just hello from each client number")
#     time.sleep(5)

import pygame as pg
import sys
import time
from game import Game
from gui import Board
from network import Network

n = Network()
n.connect()
game = Game()
gui = Board()
status = 'next'


def process_click():
    global status
    pos = pg.mouse.get_pos()
    row, col = gui.detect_square(pos)
    if game.is_free(row, col):
        gui.mark_board(row, col, game.turn)
        game.make_move(row, col)
        if game.winner:
            gui.cross_winner(game.winner_idx, game.winner_direction)
            status = 'win'
            game.turn = game.winner
        elif game.tie:
            status = 'tie'
        gui.display_game_status(status, game.turn)
        pg.display.update()


gui.game_initiating_window()
gui.display_game_status(status, game.turn)

while True:
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            n.send('eventof click,Clicked!')
            process_click()
            if game.is_over:
                print('Game over with status', status, game.turn)
                gui.display_game_status(status, game.turn)
                pg.display.update()
                time.sleep(2)
                pg.time.Clock().tick(1000)
                game.reset()
                status = "next"
                gui.game_initiating_window()
                gui.display_game_status(status, game.turn)

    pg.time.Clock().tick(10)
