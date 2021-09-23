import _thread
import socket
import pickle
import asyncio
import time

import websockets
import random
from gui import Board
import pygame as pg


class Network:
    def __init__(self):
        self.uri = "ws://localhost:5000"
        self.player = None
        self.tasks = None
        self.loop = None
        # print('self.p', self.p)
        # print("Received from server initial position", self.p)

    def get_player(self):
        return self.player

    async def producer_handler(self, ws):
        print('Im in client producer handler')
        message = await self.tasks.get()
        await ws.send(message)


    async def consumer_handler(self,ws):
        try:
            event, message = (await ws.recv()).split(",")
            if event == 'init':
                self.player = message
                # gui.game_initiating_window()
                # gui.display_game_status(status, player)
                # pg.display.update()

                print("Received from server: i'm player ", self.player)
            print('And my websocket number is', ws)
            # await all_messages.put((message, ws))

        except Exception as error:
            print(error)

    def handler(self):
        async def run():
            self.tasks = asyncio.Queue()
            self.loop = asyncio.get_running_loop()
            async with websockets.connect(self.uri) as websocket:

                while True:

                    listener_task = asyncio.ensure_future(self.consumer_handler(websocket))
                    producer_task = asyncio.ensure_future(self.producer_handler(websocket))
                    print('listener  and producer', listener_task,producer_task)
                    done, pending = await asyncio.wait(
                        [listener_task, producer_task],
                        return_when=asyncio.FIRST_COMPLETED)
                    for task in pending:
                        task.cancel()
                    await asyncio.sleep(2)
        asyncio.run(run())

        # asyncio.get_event_loop().run_forever()
    def connect(self):

        _thread.start_new_thread(self.handler,())
        while not self.loop:
            time.sleep(1)
        # _thread.start_new_thread(asyncio.get_event_loop().run_until_complete(self.handler()),())

    def send(self, message):
        print ("Inside function ssend")
        # while self.loop is None: time.sleep(1)
        self.loop.call_soon_threadsafe(lambda: self.tasks.put_nowait(message))

        print('list of tasks', self.tasks)



#     def send(self, data):
#         try:
#             # self.client.send(pickle.dumps(data))
#             # we are sending the string but receiving pbject
#             self.client.send(str.encode(data))
#             return pickle.loads(self.client.recv(2048))
#         except socket.error as error:
#             print(error)
#
#
#
#
#     # global all_messages
#     # (message, sender) = await all_messages.get()
#     # i = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
#     # if i == 1:
#     #     message = f"Hi,{ws}"
#     #     await ws.send(message)
#     # print(f"<received from server {greeting}")
#
#
#
#
# # run_until_complete(hello())
#
#
#

