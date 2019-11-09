import time
import urllib
import hashlib
import hmac


class BitMEXAuth:
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
            self.generated_url,
            [
                ("api-expires", expires),
                ("api-signature", signature),
                ("api-key", apiKey),
            ],
        )

