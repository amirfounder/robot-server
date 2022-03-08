import asyncio
import json
import websockets
from websockets.server import WebSocketServerProtocol
from handler import handle_message


async def handler(websocket: WebSocketServerProtocol):
    while True:
        if (message := await websocket.recv()):
            print(message)
            try:
                x = json.loads(message)
                for y in x:
                    print(y)
                print(len(x))
            except:
                pass
            response = handle_message(message)
            await websocket.send(response or 'Done')
            print('sent message')


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())