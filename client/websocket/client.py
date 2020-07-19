import asyncio
import websockets
import sys
import time

url = "ws://52.221.248.198:8080"
n_times = 5
delay_ms = 200

with open("./../../test_img/640x640.jpg", "rb") as image:
  f = image.read()
  binary_img = bytearray(f)
  print(sys.getsizeof(binary_img))


async def hello():
    async with websockets.connect(url) as websocket:
        time.sleep(1)
        for i in range(n_times):
            message = bytes(str(int(time.time()*1000)), 'utf-8') + binary_img
            print('n_times: {}'.format(i))
            await websocket.send(message)
            time.sleep(delay_ms/1000)

asyncio.get_event_loop().run_until_complete(hello())
