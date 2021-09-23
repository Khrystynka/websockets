import time
from  network import Network
n=Network()
n.connect()

while True:
    print('Is it goint to be here?')
    n.send(f"just hello from each client number")
    time.sleep(5)