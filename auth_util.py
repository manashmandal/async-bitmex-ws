import time
import urllib
import hashlib
import hmac
import websockets
from websockets.protocol import State
import asyncio
import json
import math

def find_by_keys(keys, table, matchData):
    for item in table:
        if all(item[k] == matchData[k] for k in keys):
            return item


def order_leaves_quantity(o):
    if o["leavesQty"] is None:
        return True
    return o["leavesQty"] > 0


class BitMEXWS:
    def __init__(
        self,
        apiKey: str,
        secret: str,
        testnet: bool,
        subscriptions=None,
        symbol="XBTUSD",
        timeout=3600,
    ):
        self.symbol_subs = []
        self.non_symbol_subs = []
        self.symbol = symbol
        self.timeout = timeout
        self.testnet = testnet
        self.apiKey = apiKey
        self.secret = secret

        if not subscriptions:
            self.symbol_subs = ["instrument", "order", "position"]
            self.non_symbol_subs = ["margin"]
        else:
            self.symbol_subs = subscriptions.get("symbol_subs")
            self.non_symbol_subs = subscriptions.get("non_symbol_subs")

        self.subscriptions = [
            f"{sub}:{self.symbol}" for sub in self.symbol_subs
        ] + self.non_symbol_subs

        self.data = {}
        self.keys = {}
        self.MAX_TABLE_LEN = 50

    def __generate_nonce(self):
        return str(int(round(time.time()) + self.timeout))

    def __get_url(self):
        if self.testnet:
            self.endpoint = "https://testnet.bitmex.com/api/v1"
        else:
            self.endpoint = "https://bitmex.com/api/v1"

        urlParts = list(urllib.parse.urlparse(self.endpoint))
        urlParts[0] = urlParts[0].replace("http", "ws")
        urlParts[2] = "/realtime?subscribe={}".format(",".join(self.subscriptions))

        self.generated_url = urllib.parse.urlunparse(urlParts)
        return self.generated_url

    def __generate_signature(self, nonce):
        verb = "GET"
        url = "/realtime"
        nonce = nonce
        data = ""

        parsedURL = urllib.parse.urlparse(url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + "?" + parsedURL.query

        message = (verb + path + str(nonce) + data).encode("utf-8")

        signature = hmac.new(
            self.secret.encode("utf-8"), message, digestmod=hashlib.sha256
        ).hexdigest()
        return signature

    # Get auth for python websockets
    def get_url_auth(self):

        nonce = self.__generate_nonce()
        expires = nonce
        signature = self.__generate_signature(nonce)
        apiKey = self.apiKey

        return (
            self.__get_url(),
            [
                ("api-expires", expires),
                ("api-signature", signature),
                ("api-key", apiKey),
            ],
        )

    async def receive_message(self):
        await asyncio.sleep(1)
        async for message in self.ws:
            # self.data = message
            self.__on_message(message)
            # print("message")
            # await asyncio.sleep(1)

    async def connect(self):
        url, headers = self.get_url_auth()
        self.ws = await websockets.connect(url, extra_headers=headers)
        return self.ws.open

    def state(self):
        return self.ws.state

    def is_alive(self):
        print(self.ws.state)
        return self.ws.state == State.OPEN

    async def close(self):
        print("GRACEFULLY CLOSING THE SOCKET")
        await self.ws.close()

    # Fetch required data
    def get_instrument(self):
        '''Get the raw instrument data for this symbol.'''
        # Turn the 'tickSize' into 'tickLog' for use in rounding
        instrument = self.data['instrument'][0]
        instrument['tickLog'] = int(math.fabs(math.log10(instrument['tickSize'])))
        return instrument

    
    def funds(self):
        '''Get your margin details.'''
        return self.data['margin'][0]

    

    def __on_message(self, message):
        """Handler for parsing WS messages."""
        message = json.loads(message)

        table = message.get("table")
        action = message.get("action")
        try:
            if "subscribe" in message:
                self.logger.debug("Subscribed to %s." % message["subscribe"])
            elif action:
                if table not in self.data:
                    self.data[table] = []

                # There are four possible actions from the WS:
                # 'partial' - full table image
                # 'insert'  - new row
                # 'update'  - update row
                # 'delete'  - delete row
                if action == "partial":
                    self.data[table] = message["data"]
                    # Keys are communicated on partials to let you know how to uniquely identify
                    # an item. We use it for updates.
                    self.keys[table] = message["keys"]
                elif action == "insert":
                    self.data[table] += message["data"]

                    # Limit the max length of the table to avoid excessive memory usage.
                    # Don't trim orders because we'll lose valuable state if we do.
                    if (
                        table not in ["order"]
                        and len(self.data[table]) > self.MAX_TABLE_LEN
                    ):
                        self.data[table] = self.data[table][self.MAX_TABLE_LEN // 2 :]

                elif action == "update":
                    # Locate the item in the collection and update it.
                    for updateData in message["data"]:
                        item = find_by_keys(
                            self.keys[table], self.data[table], updateData
                        )
                        if not item:
                            return  # No item found to update. Could happen before push
                        item.update(updateData)
                        # Remove cancelled / filled orders
                        if table == "order" and not order_leaves_quantity(item):
                            self.data[table].remove(item)
                elif action == "delete":
                    # Locate the item in the collection and remove it.
                    for deleteData in message["data"]:
                        item = find_by_keys(
                            self.keys[table], self.data[table], deleteData
                        )
                        self.data[table].remove(item)
                else:
                    raise Exception("Unknown action: %s" % action)
        except Exception as exe:
            # self.logger.error(traceback.format_exc())
            print(str(exe), exe.__class__.__name__)

