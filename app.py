from sanic import Sanic
import socketio
from sanic import response
import psutil

# from async_bitmex_ws import run_bitmex
from multiprocessing import Process
import asyncio
from async_bitmexws import init_bitmex


app = Sanic()
p = Process()
sio = socketio.AsyncClient()

apiKey = "F061zxLTOGYyPMlwq-EU4YaW"
apiSecret = "uIOiJzEhhHK5oiC3v1M6nYskIlFKAdtg_Jc966EUsO7TqQPy"


async def connect_socketio():
    if not sio.connected:
        await sio.connect("http://localhost:4000")


@app.route("/", methods=["GET"])
async def index(request):
    return response.json({"hey": "asd"})


@app.route("/socket", methods=["GET"])
async def connect_socket(request):
    socketio_task = asyncio.create_task(connect_socketio())
    return response.json({"connected": "ok", "name": str(socketio_task)})


@app.route("/start-socket", methods=["GET"])
async def start_socket(request):
    await connect_socketio()

    socket_exists = all(
        [
            any(["init_bitmex" in str(task) for task in asyncio.all_tasks()]),
            sio.connected,
        ]
    )

    print(f"socket existws {socket_exists}")

    if socket_exists:
        return response.json(
            {"error": "A socket is already running, disconnect it first then try"},
            status=400,
        )

    else:
        task = asyncio.create_task(
            init_bitmex(socketio=sio, apiKey=apiKey, secret=apiSecret, testnet=True)
        )
        print(task)

    return response.json({"message": "started"})

@app.route("/stop-socket", methods=["GET"])
async def stop_socket(request):
    await sio.disconnect()
    for task in asyncio.all_tasks():
        if "init_bitmex" in str(task) or "connect_socketio" in str(task):
            task.cancel()
            await asyncio.sleep(1)
            print(f"TASK CANCELED {task.cancelled()}")

    return response.json({"hey": "lo"})
  


app.run(host="0.0.0.0", port=5000, debug=True)
