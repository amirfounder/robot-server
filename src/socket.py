import asyncio
import json
from threading import Thread
from typing import Callable
import websockets
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed
from src.handler import handle_message_data
import webbrowser


class WebSocketServer:

    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

    def __init__(self) -> None:
        self.url_connection_map: dict[str, WebSocketServerProtocol] = {}
        self.is_waiting_for_new_connection: bool = False
        self.callback_on_new_connection_callback: Callable = None
    
    def open_url(self, url: str) -> tuple[str, WebSocketServerProtocol]:
        if url in self.url_connection_map.keys():
            print('Connection with url already exists ...')
            return url, self.url_connection_map.get(url)

        webbrowser.get(self.chrome_path).open(url)

    def wait_for_connection(self):
        print('waiting for connection ...')
        self.is_waiting_for_new_connection = True
        self.new_connection_url = None

        def on_new_connection_callback(url: str):
            self.new_connection_url = url
            self.is_waiting_for_new_connection = False

        self.on_new_connection_callback = on_new_connection_callback

        while self.is_waiting_for_new_connection:
            pass
        
        print('waiting for connection completed!')
        return self.new_connection_url, self.url_connection_map.get(self.new_connection_url)

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

    def start_task(self, url: str = None, task_name: str = None, **kwargs):
        asyncio.run(self.start_task_async(url, task_name, **kwargs))

    async def start_task_async(self, url: str = None, task_name: str = None, **kwargs):
        if (connection := self.url_connection_map.get(url)):
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
        else:
            print('requested url to start task: {}'.format(url))
            print('all urls = {}'.format(str(self.url_connection_map.keys())))

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
                    response = json.dumps({
                        'requestId': id,
                        'data': response
                    })

                    print('returning message')
                    await connection.send(response)
                    print('message returned')
        
        except ConnectionClosed as e:
            url, _ = next(iter([pair for pair in self.url_connection_map.items(
            )if pair[1] == connection]), None)
            self.url_connection_map.pop(url, None)
            print(
                'Connection to URL : {} was closed and removed from our map.'.format(url))

    def get_connection(self, url):
        url_connection_pairs = self.url_connection_map.items()

        if len(url_connection_pairs) == 0:
            return None

        if len(url_connection_pairs) == 1 or not url:
            return list(url_connection_pairs)[0][1]

        if len(url_connection_pairs) == 2:
            return self.url_connection_map[url]

    def register_connection(self, url: str, connection: WebSocketServerProtocol):
        print('register_connection function called!')
        if not url:
            return

        if connection in self.url_connection_map.values():
            return

        if url in self.url_connection_map.keys():
            return

        self.url_connection_map[url] = connection
        if self.is_waiting_for_new_connection:
            self.on_new_connection_callback(url)

    def unregister_connection(self, url):
        self.url_connection_map.pop(url, None)
