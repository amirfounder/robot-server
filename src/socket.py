import asyncio
import json
from threading import Thread
import websockets
from websockets.server import WebSocketServerProtocol
from handler import handle_message_data


class WebSocketServer:

    def __init__(self) -> None:
        self.websocket_connection_map: dict[str, WebSocketServerProtocol] = {}

    def wait_until_first_connection(self):
        while len(self.websocket_connection_map.items()) == 0:
            pass

    def run_server(self):
        asyncio.run(self.serve())

    def run_server_in_separate_thread(self):
        thread = Thread(target=self.run_server, daemon=True)
        thread.start()
    
    def start_task(self, task_name: str = None, id: str = None):
        asyncio.run(self.start_task_async(task_name, id))

    async def start_task_async(self, task_name: str = None, id: str = None):
        message = {
            'requesId': None,
            'method': 'start-task',
            'data': { 'taskName': task_name }
        }

        connections = self.websocket_connection_map.items()
        
        server = None

        if len(connections) == 0:
            print('Failed to start task. No connections mapped ...')
            return

        if len(connections) == 1 or not id:
            id, server = list(connections)[0]

        server: WebSocketServerProtocol = self.websocket_connection_map[id]
        await server.send(json.dumps(message))
        

    async def handler(self, websocket: WebSocketServerProtocol):
        print('Connection received ...')
        while True:
            if (message := await websocket.recv()):
                print(message)

                message = json.loads(message)
                message_id = message.get('id')
                message_data = message.get('data', '')

                if websocket not in self.websocket_connection_map.values():
                    if isinstance(message_data, str):
                        if message_data not in self.websocket_connection_map.keys():
                            self.websocket_connection_map[message_data] = websocket

                if isinstance(message_data, list):
                    [print(x) for x in message_data]
                    response_data = 'Received hashtags'

                else:
                    response_data = handle_message_data(message_data)

                response = {
                    'requestId': message_id,
                    'data': response_data or 'Done'
                }

                response = json.dumps(response)

                await websocket.send(response)
                print('sent message')

    async def serve(self):
        async with websockets.serve(self.handler, "", 8001):
            await asyncio.Future()
