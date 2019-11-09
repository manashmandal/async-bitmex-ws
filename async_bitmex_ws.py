import websockets
import socketio
from auth_util import BitMEXWS
import asyncio
import json

apiKey = "F061zxLTOGYyPMlwq-EU4YaW"
apiSecret = "uIOiJzEhhHK5oiC3v1M6nYskIlFKAdtg_Jc966EUsO7TqQPy"

ws = BitMEXWS(apiKey=apiKey, secret=apiSecret, testnet=True)

asyncio.get_event_loop().run_until_complete(ws.connect())
