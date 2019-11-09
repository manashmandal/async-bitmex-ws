import websockets
import socketio
from auth_util import BitMEXWS
import asyncio
import json
from websockets.protocol import State
import datetime
import time

# sio = socketio.AsyncClient()

apiKey = "F061zxLTOGYyPMlwq-EU4YaW"
apiSecret = "uIOiJzEhhHK5oiC3v1M6nYskIlFKAdtg_Jc966EUsO7TqQPy"

ws = BitMEXWS(apiKey=apiKey, secret=apiSecret, testnet=True)


async def printHello(sio):
    # await sio.connect("http://localhost:4000")
    # print("hello")
    # try:
    while ws.state() == State.OPEN:
        # await asyncio.sleep(5)
        await asyncio.sleep(1)

        print(time.time(), ws.positions())
        # print(ws.data)
        # await sio.emit(
        #     "positionEvent",
        #     {"time": str(datetime.datetime.now()), "data": ws.positions()},
        # )

        # print("instrument data", ws.get_instrument())
        # print(ws.funds())
        # print(ws.open_orders())
        # print(ws.positions())
        # print(ws.funds())
        # print("funds", ws.funds())

    await ws.close()

    # if ws.state() == State.CLOSING or ws.state() == State.CLOSED:
    #     await ws.close()


async def run_bitmex():
    await ws.connect()
    # try:
    await asyncio.gather(ws.receive_message(), printHello(None))
    # await ws.receive_message()

    # except Exception as exe:
    #     print(str(exe), exe.__class__.__name__)

    # print("hol up")
    # await ws.connect()
    # ws.receive_message()
    # printHello()
    # print("hey")


# asyncio.get_event_loop().run_until_complete(ws.connect())
# asyncio.get_event_loop().run_until_complete(run_bitmex(None))
