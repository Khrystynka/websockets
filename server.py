import asyncio
import websockets
import datetime
from game import Game

all_messages = None
import pygame as pg
import sys
import time
from game import Game
from gui import Board

game = Game()
# gui = Board()
status = 'next'

all_games=dict()



#
# def process_click():
#     global status
#     pos = pg.mouse.get_pos()
#     row, col = gui.detect_square(pos)
#     if game.is_free(row, col):
#         gui.mark_board(row, col, game.turn)
#         game.make_move(row, col)
#         if game.winner:
#             gui.cross_winner(game.winner_idx, game.winner_direction)
#             status = 'win'
#             game.turn = game.winner
#         elif game.tie:
#             status = 'tie'
#         gui.display_game_status(status, game.turn)
#         pg.display.update()



async def producer_handler():
    global all_messages
    (message, sender) = await all_messages.get()
    [await w[0].send(message) for w in connected if w[0] != sender]


async def consumer_handler(ws):
    global all_messages
    try:
        message = await ws.recv()
        await all_messages.put((message, ws))
        print ('Server: All received  msgs',all_messages)

    except Exception as error:
        print(error)


connected = set()


async def handler(websocket, path):
    global all_games
    game_idx = len(connected)/2
    if not len(connected) % 2:
        player ='x'
    else:
       player = 'o'
    await websocket.send(f'init,{player}')
    connected.add((websocket,player))
    all_games[game_idx]={player: websocket}



    print('connected websockets', connected)

    while True:
        listener_task = asyncio.ensure_future(consumer_handler(websocket))
        producer_task = asyncio.ensure_future(producer_handler())

        done, pending = await asyncio.wait(
            [listener_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        await asyncio.sleep(1)

        # if listener_task in done:
        #     message = listener_task.result()
        #     await consumer(message)
        # else:
        #     listener_task.cancel()
        #
        # if producer_task in done:
        #     message = producer_task.result()
        #     await websocket.send(message)
        # else:
        #     producer_task.cancel()


async def main():
    async with websockets.serve(handler, "localhost", 5000):
        global all_messages
        all_messages = asyncio.Queue()

        await asyncio.Future()  # run forever


asyncio.run(main())
