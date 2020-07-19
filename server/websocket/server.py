import asyncio
import websockets
import sys
import time

async def hello(websocket, path):
    count = 0
    while True:
        data = await websocket.recv()
        current_timestamp = time.time()*1000
        print(sys.getsizeof(data))
        print(data[0:13])

        timestamp = int(data[0:13].decode('utf-8'))
        network_time_ms = current_timestamp - timestamp
        print('network_time_ms: {}'.format(network_time_ms))

        # Write result file
        count += 1
        with open("result.txt", "a") as file_object:
            file_object.write('{},{}\n'.format(count, network_time_ms))



start_server = websockets.serve(hello, "0.0.0.0", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
