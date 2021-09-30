import asyncio
import time

import websockets
from game import Game
import pickle
from collections import deque

active_games = dict()
all_messages = None
connected = dict()
ws_waiting = deque()
next_game = -1


async def producer_handler():
    global all_messages, connected, next_game
    message = await all_messages.get()
    print("THIS MOVW WAS FROM CLIENT", message)
    row, col, player, game_id = [int(x) for x in message.split(",")]
    if game_id not in active_games:
        return
    game = active_games[game_id]

    if player == game.turn and game.is_free(row, col):
        game.make_move(row, col)
        game.update_status()
        status = 'move'
        if game.winner:
            status = 'win'
        elif game.tie:
            status = 'tie'
        move_obj = {
            "action": "move",
            'row': row,
            "col": col,
            "player": player,
            "status": status,
            "winner_id": game.winner_idx,
            "winner_dir": game.winner_direction,
            'board': game.board
        }
        game_update_massage = pickle.dumps(move_obj)
    else:
        invalid_obj = {
            "action": "invalid",
        }
        game_update_massage = pickle.dumps(invalid_obj)
    recipients = [game.x_player, game.o_player]
    [await w.send(game_update_massage) for w in recipients if w in connected]
    if game.is_over:
        next_game += 1
        del active_games[game.id]
        time.sleep(5)
        await new_game(game.o_player, game.x_player, next_game)


async def consumer_handler(ws):
    global all_messages, connected, ws_waiting, next_game
    game_id = connected[ws]

    try:
        message = await ws.recv()
        await all_messages.put(message)

    except Exception as error:
        print('Server message:Lost connection with client!', ws, error)
        not_ready_obj = {
            "action": "not ready",
        }
        if game_id != None:
            # print("PALYERS IN THE GAME", 'x:',active_games[game_id].x_player, 'o', active_games[game_id].o_player)
            if active_games[game_id].x_player != ws:
                other_player = active_games[game_id].x_player
            else:
                other_player = active_games[game_id].o_player
            del active_games[game_id]
            if len(ws_waiting) != 0:
                opponent = ws_waiting.pop()
                next_game += 1
                await new_game(opponent, other_player, next_game)
            else:
                ws_waiting.append(other_player)
                await other_player.send(pickle.dumps(not_ready_obj))
                connected[other_player] = None
        del connected[ws]


async def new_game(x_pl, o_pl, game_idx):
    global connected, active_games
    game = Game(game_idx)
    active_games[game.id] = game
    game.x_player = x_pl
    game.o_player = o_pl
    x_message = {
        "action": "init",
        "player": 1,
        "game_id": game.id,
        "board": active_games[game_idx].board
    }
    o_message = {
        "action": "init",
        "player": 2,
        "game_id": game.id,
        "board": active_games[game.id].board
    }
    await game.x_player.send(pickle.dumps(x_message))
    await game.o_player.send(pickle.dumps(o_message))
    connected[x_pl] = game.id
    connected[o_pl] = game.id


async def handler(websocket, path):
    global active_games, ws_waiting, next_game
    opponent = None
    if len(ws_waiting) != 0:
        opponent = ws_waiting.popleft()
    if opponent:
        next_game = next_game + 1
        await new_game(opponent, websocket, next_game)
    else:
        not_ready_message = {
            "action": "not ready"
        }
        await websocket.send(pickle.dumps(not_ready_message))
        ws_waiting.append(websocket)
        connected[websocket] = None

    while websocket in connected:
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
