import asyncio
import websockets
from flask import Flask, render_template, request


clients = set()

app = Flask(__name__)

notes = {
    "1": {
        "Title": "Hello world",
        "Description": "It is a first note"
    },
    "2": {
        "Title": "Second note",
        "Description": "It is a second note"
    }
}


@app.get('/all_notes')
def main():
    return notes


@app.post('/home')
def home():
    print(dir(request))
    print(request.view_args)
    return "sdf"


async def conection_handler(websocket):
    try:
        clients.add(websocket)
        print("Client conected")
        await websocket.send("Conected to server!")

        async for msg in websocket:
            print(msg)
            await websocket.send(msg)

        await websocket.wait_closed()

    finally:
        clients.remove(websocket)
        print(f"Client disconnected. Remaining clients: {len(clients)}")


async def main():
    # tiker = asyncio.create_task(client_tiker())
    async with websockets.serve(conection_handler, "localhost", 8765):
        print("Server started")
        await asyncio.Future()


# asyncio.run(main())