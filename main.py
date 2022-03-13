from time import sleep
from src.socket import WebSocketServer
from src.profile_generators import *
from src.profile_crud import *


def start_task_get_hashtag_recommendations():
    pass


GOOGLE_ACCOUNTS_URL = 'https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin'


def main():
    profile = select_profile_by_id(1)
    socket = WebSocketServer()
    socket.run_server_in_separate_thread()

    socket.open_url(GOOGLE_ACCOUNTS_URL)
    url, _ = socket.wait_for_connection()

    socket.start_task(url, 'create-google-account-step-1')
    url, _ = socket.wait_for_connection()
    
    socket.start_task(url, 'create-google-account-step-2', profile=profile)
    url, _ = socket.wait_for_connection()

    socket.start_task(url, 'create-google-account-step-3', profile=profile)
    url, _ = socket.wait_for_connection()

    while True:
        print('waiting ...')
        sleep(5)


if __name__ == "__main__":
    main()
