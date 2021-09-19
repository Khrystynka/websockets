import asyncio
import websockets
import datetime

all_messages = None



async def producer_handler():
            global all_messages
            (message, sender) = await all_messages.get()
            [await w.send(message) for w in connected if w != sender]


async def consumer_handler(ws):
    global all_messages
    message = await ws.recv()
    await all_messages.put((message, ws))

connected = set()

async def handler(websocket, path):
    connected.add(websocket)
    print('connected websockets', connected)

    while True:
        listener_task = asyncio.ensure_future(consumer_handler(websocket))
        producer_task = asyncio.ensure_future(producer_handler())

        done, pending = await asyncio.wait(
            [listener_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

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
