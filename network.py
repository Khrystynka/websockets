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
    def __init__(self,callback):
        self.uri = "ws://localhost:5000"
        self.tasks = None
        self.loop = None
        self.callback = callback
    async def producer_handler(self, ws):
        print('Im in client producer handler')
        message = await self.tasks.get()
        await ws.send(message)


    async def consumer_handler(self,ws):
        try:
            message = (await ws.recv())
            self.callback(message)

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
                    # print('listener  and producer', listener_task,producer_task)
                    done, pending = await asyncio.wait(
                        [listener_task, producer_task],
                        return_when=asyncio.FIRST_COMPLETED)
                    for task in pending:
                        task.cancel()
                    await asyncio.sleep(2)
        asyncio.run(run())

    def connect(self):

        _thread.start_new_thread(self.handler,())
        while not self.loop:
            time.sleep(0.01)

    def send_task(self, message):
        self.loop.call_soon_threadsafe(lambda: self.tasks.put_nowait(message))

