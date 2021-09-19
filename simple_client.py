import websocket
import _thread
import time


def on_message(ws, message):
    print("received message:", message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        while True:
            time.sleep(1)
            name = input("enter the name")
            ws.send(name)
        time.sleep(1)
        # ws.close()
        # print("thread terminating...")
    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5000/",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
