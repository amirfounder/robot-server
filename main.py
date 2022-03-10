from time import sleep, time
import webbrowser
from src.socket import WebSocketServer


def main():
    socket = WebSocketServer()
    socket.run_server_in_separate_thread()

    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    url = 'https://www.google.com'
    webbrowser.get(chrome_path).open(url)

    socket.wait_until_first_connection()
    socket.start_task('query-hashtags')

    while True:
        print('waiting ...')
        sleep(5)


if __name__ == "__main__":
    main()
