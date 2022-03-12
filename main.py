from time import sleep
import webbrowser
from src.socket import WebSocketServer


def main():
    socket = WebSocketServer()
    socket.run_server_in_separate_thread()

    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

    webbrowser.get(chrome_path).open('https://instagram.com/')
    
    socket.wait_until_first_connection()
    socket.start_task('https://instagram.com/', 'get-hashtag-recommendations', startingHashtag='#blue')

    while True:
        print('waiting ...')
        sleep(5)


if __name__ == "__main__":
    main()
