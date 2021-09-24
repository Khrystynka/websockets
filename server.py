import asyncio
import websockets
from game import Game

all_games = dict()
all_messages = None


async def producer_handler():
    global all_messages
    message = await all_messages.get()
    row, col, player, game_id = [int(x) for x in message.split(",")]
    if game_id not in all_games:
        return
    game = all_games[game_id]
    if not game.ready:
        game_update_massage = "no game"
    elif game.ready and player == game.turn and game.is_free(row, col):
        game.make_move(row, col)
        game.update_status()
        status = 'move'
        if game.winner:
            status = 'win'
        elif game.tie:
            status = 'tie'
        game_update_massage = f"move,{row},{col},{player},{status},{game.winner_idx},{game.winner_direction}"
    else:
        game_update_massage = f"invalid move"
    recipients = [game.x_player, game.o_player]
    [await w.send(game_update_massage) for w in recipients]


async def consumer_handler(ws):
    global all_messages
    try:
        message = await ws.recv()
        await all_messages.put(message)
        print('Server: All received  msgs', all_messages)

    except Exception as error:
        print(error)


connected = set()


async def handler(websocket, path):
    global all_games
    game_idx = len(connected) // 2
    if game_idx not in all_games:
        all_games[game_idx] = Game()
    if not len(connected) % 2:
        all_games[game_idx].x_player = websocket
        player = 1
        await websocket.send(f'not ready')
    else:
        all_games[game_idx].o_player = websocket
        all_games[game_idx].ready = True
        player = 2
        await websocket.send(f'init,{player},{game_idx}')
        await all_games[game_idx].x_player.send(f'init,1,{game_idx}')



    connected.add((websocket, player, game_idx))
    # print("Games connected sofar", all_games)
    #
    # print('connected websockets', connected)

    while True:
        listener_task = asyncio.ensure_future(consumer_handler(websocket))
        producer_task = asyncio.ensure_future(producer_handler())

        done, pending = await asyncio.wait(
            [listener_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(handler, "localhost", 5000):
        global all_messages
        all_messages = asyncio.Queue()

        await asyncio.Future()  # run forever


asyncio.run(main())
