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


@app.route("/start-socket", methods=["GET"])
async def start_socket(request):
    # await sio.connect("http://localhost:4000")
    # p = Process(target=run, args=(sio,))
    # p.start()
    # p.join()
    task = asyncio.create_task(run_bitmex())  # , loop=asyncio.get_event_loop())
    # Wait for the thread to join
    # await asyncio.sleep(3)
    print(task)

    # return response.json({"pid": p.pid})
    return response.json({"hey": "ya"})


@app.route("/stop-socket", methods=["GET"])
async def stop_socket(request):

    print(asyncio.all_tasks())
    for task in asyncio.all_tasks():
        if "printHello" in str(task):
            task.cancel()
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
