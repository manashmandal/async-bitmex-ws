from sanic import Sanic
import socketio
from sanic import response
import psutil
from async_bitmex_ws import run_bitmex
from multiprocessing import Process
import asyncio

psid = None

app = Sanic()
p = Process()
sio = socketio.AsyncClient()


def run(sio):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_bitmex())
    loop.close()


@app.route("/", methods=["GET"])
async def index(request):
    return response.json({"hey": "asd"})


@app.route("/start-socket", methods=["GET"])
async def start_socket(request):
    # await sio.connect("http://localhost:4000")
    p = Process(target=run, args=(sio,))
    p.start()

    # Wait for the thread to join
    await asyncio.sleep(3)

    return response.json({"pid": p.pid})


@app.route("/stop-socket", methods=["GET"])
async def stop_socket(request):
    # await sio.disconnect()
    print(request.json)
    body = request.json
    status = psutil.Process(pid=body["pid"]).kill()
    print(status)
    return response.json({"status": status})


app.run(host="0.0.0.0", port=5000)
