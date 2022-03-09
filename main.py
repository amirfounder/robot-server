import asyncio
import json
import websockets
import time
from websockets.server import WebSocketServerProtocol
from handler import handle_message_data


async def handler(websocket: WebSocketServerProtocol):
    while True:
        if (message := await websocket.recv()):
            print(message)
            time.sleep(.5)

            message = json.loads(message)
            message_id = message.get('id')
            message_data = message.get('data','')

            if isinstance(message_data, list):
                [print(x) for x in message_data]
                response_data = 'Received hashtags'

            else:
                response_data = handle_message_data(message_data)

            response = {
                'id': message_id,
                'data': response_data or 'Done'
            }

            response = json.dumps(response)

            await websocket.send(response)
            print('sent message')


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())