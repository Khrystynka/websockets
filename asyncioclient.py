import asyncio
import websockets
import random
from gui import Board
import pygame as pg
import _thread

gui = Board()
status = 'next'
player ='x'
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




# while True:
#     pg.display.update()
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             pg.quit()
#             sys.exit()
#         elif event.type == pg.MOUSEBUTTONDOWN:
#             print('Clicked!')
#             process_click()
#             if game.is_over:
#                 print('Game over with status',status,game.turn)
#                 gui.display_game_status(status,game.turn)
#                 pg.display.update()
#                 time.sleep(2)
#                 pg.time.Clock().tick(1000)
#                 game.reset()
#                 status = "next"
#                 gui.game_initiating_window()
#                 gui.display_game_status(status, game.turn)
#
#     pg.time.Clock().tick(10)
async def producer_handler(ws):
    pass
    # global all_messages
    # (message, sender) = await all_messages.get()
    # i = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    # if i == 1:
    #     message = f"Hi,{ws}"
    #     await ws.send(message)
    # print(f"<received from server {greeting}")


async def consumer_handler(ws):
    global player
    try:
        event, message = (await ws.recv()).split(",")
        if event == 'init':
            player = message
            gui.game_initiating_window()
            gui.display_game_status(status, player)
            pg.display.update()

            print("Received from server: i'm player ", message)
        print('And my websocket number is', ws)
        # await all_messages.put((message, ws))

    except Exception as error:
        print(error)


async def hello():
    uri = "ws://localhost:5000"
    global status, player

    async with websockets.connect(uri) as websocket:

        while True:

            listener_task = asyncio.ensure_future(consumer_handler(websocket))
            producer_task = asyncio.ensure_future(producer_handler(websocket))

            done, pending = await asyncio.wait(
                [listener_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            await asyncio.sleep(2)


asyncio.get_event_loop().run_until_complete(hello())
# run_until_complete(hello())
