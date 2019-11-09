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


async def connect_socketio():
    if not sio.connected:
        await sio.connect("http://localhost:4000")


# async def disconnect_socketio():
#     await sio.disconnect()


# loop = asyncio.get_event_loop()


# loop = asyncio.get_event_loop()


def run(sio):
    # asyncio.gather(run_bitmex(),)
    print(asyncio.get_event_loop().run_until_complete())
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(run_bitmex())
    # loop.close()
    # loop.close()


@app.route("/", methods=["GET"])
async def index(request):
    return response.json({"hey": "asd"})


@app.route("/socket", methods=["GET"])
async def connect_socket(request):
    socketio_task = asyncio.create_task(connect_socketio())
    return response.json({"connected": "ok", "name": str(socketio_task)})


@app.route("/start-socket", methods=["GET"])
async def start_socket(request):

    try:
        no_print_hello = True
        for task in asyncio.all_tasks():
            if "printHello" in str(task):
                no_print_hello = False

        if no_print_hello == True:
            # asyncio.create_task(connect_socketio())
            # await sio.connect("http://localhost:4000")
            socketio_task = asyncio.create_task(connect_socketio())
            task = asyncio.create_task(run_bitmex(sio=sio))  # ,
            print(task)
            print(socketio_task)
    except Exception as exe:
        print(exe)

    # return response.json({"pid": p.pid})
    return response.json({"hey": "ya"})


@app.route("/stop-socket", methods=["GET"])
async def stop_socket(request):
    # await sio.disconnect()
    # print(asyncio.all_tasks())
    # asyncio.create_task(disconnect_socketio())
    # await sio.disconnect()
    for task in asyncio.all_tasks():
        if "run_bitmex" in str(task) or "connect_socketio" in str(task):
            task.cancel()
            await asyncio.sleep(1)
            print(f"TASK CANCELED {task.cancelled()}")
            # print(task)

    return response.json({"hey": "lo"})
    # await sio.disconnect()
    # print(request.json)
    # body = request.json
    # status = psutil.Process(pid=body["pid"]).kill()
    # print(status)
    # asyncio.tasks.
    # return response.json({"status": status})


# server = app.create_server(host="0.0.0.0", port=5000, return_asyncio_server=True)
# task = asyncio.ensure_future(server)
# loop.run_forever()
app.run(host="0.0.0.0", port=5000)
