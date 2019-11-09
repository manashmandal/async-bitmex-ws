import websockets
import socketio
from auth_util import BitMEXWS
import asyncio
import json
from websockets.protocol import State

apiKey = "F061zxLTOGYyPMlwq-EU4YaW"
apiSecret = "uIOiJzEhhHK5oiC3v1M6nYskIlFKAdtg_Jc966EUsO7TqQPy"

ws = BitMEXWS(apiKey=apiKey, secret=apiSecret, testnet=True)


async def printHello():
    # print("hello")
    # try:
    while ws.state() == State.OPEN:
        await asyncio.sleep(1)
        print(ws.data)

    await ws.close()

    # if ws.state() == State.CLOSING or ws.state() == State.CLOSED:
    #     await ws.close()


async def run():
    await ws.connect()
    try:
        await asyncio.gather(ws.receive_message(), printHello())
    except Exception as exe:
        print(str(exe), exe.__class__.__name__)

    # print("hol up")
    # await ws.connect()
    # ws.receive_message()
    # printHello()
    # print("hey")


# asyncio.get_event_loop().run_until_complete(ws.connect())
asyncio.get_event_loop().run_until_complete(run())
