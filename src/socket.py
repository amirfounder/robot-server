import asyncio
import json
from threading import Thread
import websockets
from websockets.server import WebSocketServerProtocol
from src.handler import handle_message_data


class WebSocketServer:

    def __init__(self) -> None:
        self.websocket_connection_map: dict[str, WebSocketServerProtocol] = {}

    def wait_until_first_connection(self):
        while len(self.websocket_connection_map.items()) == 0:
            pass

    def run_server_in_separate_thread(self):
        thread = Thread(target=self.run_server, daemon=True)
        thread.start()

    def run_server(self):
        asyncio.run(self.serve())

    async def serve(self):
        async with websockets.serve(self.handler, "", 8001):
            await asyncio.Future()

    def run_server_in_separate_thread(self):
        thread = Thread(target=self.run_server, daemon=True)
        thread.start()

    def start_task(self, task_name: str = None, id: str = None):
        asyncio.run(self.start_task_async(task_name, id))

    def get_connection(self, id):
        id_connection_pairs = self.websocket_connection_map.items()

        if len(id_connection_pairs) == 0:
            return None

        if len(id_connection_pairs) == 1 or not id:
            return list(id_connection_pairs)[0][1]

        if len(id_connection_pairs) == 2:
            return self.websocket_connection_map[id]

    async def start_task_async(self, task_name: str = None, id: str = None):
        connection = self.get_connection(id)
        await connection.send(json.dumps({
            'requesId': None,
            'method': 'start-task',
            'data': {'name': task_name}
        }))

    async def handler(self, connection: WebSocketServerProtocol):
        print('Connection received ...')
        while True:
            if (message := await connection.recv()):
                print(message)

                message = json.loads(message)
                id = message.get('id')
                data = message.get('data', {})
                method = message.get('method')

                if method == 'register-connection':
                    self.register_connection(data.get('url'), connection)

                if method == 'unregister-connection':
                    self.unregister_connection(data.get('url'), connection)

                response = handle_message_data(data)

                await connection.send(json.dumps({
                    'requestId': id,
                    'data': response
                }))

                print('returned message')

    def register_connection(self, url: str, connection: WebSocketServerProtocol):
        if not url:
            return

        if connection in self.websocket_connection_map.values():
            return

        if url in self.websocket_connection_map.keys():
            return

        self.websocket_connection_map[url] = connection

    def unregister_connection(self, url):
        self.websocket_connection_map.pop(url, None)
