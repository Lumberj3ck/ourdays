import asyncio
import websockets

clients = set()

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


asyncio.run(main())