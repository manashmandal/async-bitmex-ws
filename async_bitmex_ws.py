import websockets
import socketio
from async_bitmexws import AsyncBitMEXWS
import asyncio
import json
from websockets.protocol import State
import datetime
import time

# sio = socketio.AsyncClient()

apiKey = "F061zxLTOGYyPMlwq-EU4YaW"
apiSecret = "uIOiJzEhhHK5oiC3v1M6nYskIlFKAdtg_Jc966EUsO7TqQPy"

# ws = BitMEXWS(apiKey=apiKey, secret=apiSecret, testnet=True)


# async def printHello(sio):
#     # print("printHello")
#     # await sio.connect("http://localhost:4000")
#     # print("hello")
#     # try:
#     while ws.state() == State.OPEN:
#         # await asyncio.sleep(5)
#         await asyncio.sleep(0.1)

#         # ws.positions()
#         # print(time.time(), ws.positions())
#         # print(ws.data)
#         await sio.emit(
#             "positionEvent",
#             {"time": str(datetime.datetime.now()), "data": ws.positions()},
#         )


#         # print("instrument data", ws.get_instrument())
#         # print(ws.funds())
#         # print(ws.open_orders())
#         # print(ws.positions())
#         # print(ws.funds())
#         # print("funds", ws.funds())

#     await ws.close()

#     # if ws.state() == State.CLOSING or ws.state() == State.CLOSED:
#     #     await ws.close()


# async def run_bitmex(sio):
#     await ws.connect()
#     # try:
#     await asyncio.gather(ws.receive_message(), printHello(sio))
#     # await ws.receive_message()

#     # except Exception as exe:
#     #     print(str(exe), exe.__class__.__name__)

#     # print("hol up")
#     # await ws.connect()
#     # ws.receive_message()
#     # printHello()
#     # print("hey")


# # asyncio.get_event_loop().run_until_complete(ws.connect())
# # asyncio.get_event_loop().run_until_complete(run_bitmex(None))
from async_bitmexws import init_bitmex


async def run_task():
    task = asyncio.create_task(
        init_bitmex(None, apiKey=apiKey, secret=apiSecret, testnet=True)
    )
    print(task)

    await task


# asyncio.get_event_loop().run_until_complete(
#     init_bitmex(None, apiKey=apiKey, secret=apiSecret, testnet=True)
# )


# print(task)

asyncio.get_event_loop().run_until_complete(run_task())

