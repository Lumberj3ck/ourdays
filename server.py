import asyncio
import websockets

clients = set()

async def client_tiker():
    while True:
        await asyncio.sleep(0.1)

        for client in clients:
            try:
                print("Plus two")
                await client.send("add")
            except websockets.exceptions.ConnectionClosed:
                print("Plus one")
                pass

async def recv_msg(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(message)
        except websockets.exceptions.ConnectionClosedOK:
            break

async def end_server(websocket):
    await websocket.wait_closed()

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

async def conection_handler_equvivalent(websocket):
    try:
        clients.add(websocket)
        print("Client conected")
        await websocket.send("Conected to server!")

        receiver = asyncio.create_task(recv_msg(websocket))
        gracefully_finish = asyncio.create_task(end_server(websocket))

        await receiver, gracefully_finish
    finally:
        clients.remove(websocket)
        print(f"Client disconnected. Remaining clients: {len(clients)}")



async def main():
    # tiker = asyncio.create_task(client_tiker())
    async with websockets.serve(conection_handler_equvivalent, "localhost", 8765):
        print("Server started")
        await asyncio.Future()


asyncio.run(main())