import asyncio
import json
from threading import Thread
from time import sleep
import websockets
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed
from src.handler import handle_message_data
import webbrowser


class WebSocketServer:

    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

    def __init__(self) -> None:
        self.websocket_connection_map: dict[str,
                                            dict[str, WebSocketServerProtocol | int]] = {}

    def open_url_and_wait_for_connection(self, url: str):
        if url in self.websocket_connection_map.keys():
            print('URL with connection')
        url_connection_pairs = self.websocket_connection_map.items()

        webbrowser.get(self.chrome_path).open(url)
        while True:
            url, connection = self.websocket_connection_map.get(url)


    def wait_until_first_connection(self):
        first_connection_made = False        
        while True:
            first_connection_made = len(self.websocket_connection_map.items()) == 1
            if first_connection_made:
                break

        print('first connection receieved!')

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

    def start_task(self, task_name: str = None, url: str = None, **kwargs):
        asyncio.run(self.start_task_async(task_name, url, **kwargs))

    async def start_task_async(self, url: str = None, task_name: str = None, **kwargs):
        if (connection := self.get_connection(url)):
            message = {
                'requestId': None,
                'data': {
                    'method': 'start-task',
                    'name': task_name,
                }
            }
            message.get('data', {}).update(kwargs)
            message = json.dumps(message)
            await connection.send(message)
            print(f'sent message ... {message}')

    async def handler(self, connection: WebSocketServerProtocol):
        print('Connection received ...')
        try:
            while True:
                if (message := await connection.recv()):
                    print(message)

                    message = json.loads(message)
                    id = message.get('id')
                    data = message.get('data', {})
                    method = data.get('method')

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
        except ConnectionClosed as e:
            url, _ = next(iter([pair for pair in self.websocket_connection_map.items()if pair[1] == connection]), None)
            self.websocket_connection_map.pop(url, None)

    def get_connection(self, url):
        url_connection_pairs = self.websocket_connection_map.items()

        if len(url_connection_pairs) == 0:
            return None

        if len(url_connection_pairs) == 1 or not url:
            return list(url_connection_pairs)[0][1]

        if len(url_connection_pairs) == 2:
            return self.websocket_connection_map[url]

    def register_connection(self, url: str, connection: WebSocketServerProtocol):
        print('register_connection function called!')
        if not url:
            return

        if connection in self.websocket_connection_map.values():
            return

        if url in self.websocket_connection_map.keys():
            return

        self.websocket_connection_map[url] = connection

    def unregister_connection(self, url):
        self.websocket_connection_map.pop(url, None)
