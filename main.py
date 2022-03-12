from time import sleep
import webbrowser
from src.socket import WebSocketServer


def main():
    socket = WebSocketServer()
    socket.run_server_in_separate_thread()

    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

    webbrowser.get(chrome_path).open('https://accounts.google.com/')
    
    socket.wait_until_first_connection()
    # socket.start_task('https://instagram.com/', 'get-hashtag-recommendations', startingHashtag='#blue')
    new_profile = dict(firstName='lol', lastName='hehe')
    socket.start_task('https://accounts.google.com/', 'create-google-account', profile=new_profile)

    while True:
        print('waiting ...')
        sleep(5)


if __name__ == "__main__":
    main()
