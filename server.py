import asyncio
import websockets
from game import Game
import pickle
from collections import deque
all_games = dict()
all_messages = None
connected = dict()
games_waiting = deque()


async def producer_handler():
    global all_messages, connected
    message = await all_messages.get()
    row, col, player, game_id = [int(x) for x in message.split(",")]
    if game_id not in all_games:
        return
    game = all_games[game_id]
    if not game.ready:
        not_ready_obj = {
            "action": "not ready",
        }
        game_update_massage = pickle.dumps(not_ready_obj)
    elif game.ready and player == game.turn and game.is_free(row, col):
        game.make_move(row, col)
        game.update_status()
        status = 'move'
        if game.winner:
            status = 'win'
        elif game.tie:
            status = 'tie'
        move_obj= {
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
        if game.is_over or not game.ready:
            game.reset()

    else:
        invalid_obj = {
            "action": "invalid",
        }
        game_update_massage = pickle.dumps(invalid_obj)
    recipients = [game.x_player, game.o_player]
    [await w.send(game_update_massage) for w in recipients if w in connected]


async def consumer_handler(ws):
    global all_messages, connected, games_waiting
    try:
        message = await ws.recv()
        await all_messages.put(message)
        print('Server: All received  msgs', all_messages)

    except Exception as error:
        print('Server message:Lost connection with client!')
        game_id = connected[ws]
        game = all_games[game_id]
        if game.x_player == ws:
            if game.o_player:
                games_waiting.append(game_id)
                game.ready =False
                game.reset()
                game.x_player = None
            else:
                games_waiting.remove(game_id)
                del all_games[game_id]
        else:
            if game.x_player:
                games_waiting.append(game_id)
                game.ready =False
                game.reset()
                game.o_player = None
            else:
                games_waiting.remove(game_id)
                del all_games[game_id]

        del connected[ws]
        await all_messages.put(f"-1,-1,-1,{game_id}")


async def handler(websocket, path):
    global all_games, games_waiting

    if len(games_waiting) !=0:
        game_idx = games_waiting.popleft()
    else:
        game_idx = len(connected) // 2
    if game_idx not in all_games:
        all_games[game_idx] = Game()
    x_message = {
            "action": "init",
            "player": 1,
            "game_id": game_idx,
            "board": all_games[game_idx].board
        }
    o_message = {
            "action": "init",
            "player": 2,
            "game_id": game_idx,
            "board": all_games[game_idx].board
        }

    not_ready_message = {
        "action": "not ready"
    }

    if not all_games[game_idx].x_player:
        all_games[game_idx].x_player = websocket
        if all_games[game_idx].o_player:
            all_games[game_idx].ready = True
            if game_idx in games_waiting:
                games_waiting.remove(game_idx)
        else:
            all_games[game_idx].ready = False
            await all_games[game_idx].x_player.send(pickle.dumps(not_ready_message))

            games_waiting.append(game_idx)
    else:
        all_games[game_idx].o_player = websocket
        if game_idx in games_waiting:
            games_waiting.remove(game_idx)
        all_games[game_idx].ready = True
    if all_games[game_idx].ready:
        all_games[game_idx].reset()
        await all_games[game_idx].x_player.send(pickle.dumps(x_message))
        await all_games[game_idx].o_player.send(pickle.dumps(o_message))

    connected[websocket] = game_idx

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
