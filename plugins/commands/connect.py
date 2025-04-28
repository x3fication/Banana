from plugins.common import *
import requests

def connect(username, server):
    try:
        response = requests.post('http://localhost:6969/connect', json={
            "host": server, "port": 25565, "username": username
        })

        if response.status_code != 200 and response.status_code != 400:
            return error(f'Failed to connect [{response.status_code}]')

        while not requests.get('http://localhost:6969/status').json().get('connected'):
            info('Waiting for connection...')
            time.sleep(1)
            pass
        
        info(f'Type "exit" to exit. [beta] this is still very shit but it works for sending messages')
        while True: 
            msg = input('> ').strip()
            if msg.lower() == "exit":
                if requests.get('http://localhost:6969/status').json().get('connected'):
                    requests.post('http://localhost:6969/disconnect')
                    info(f'Bot disconnected.')
                else:
                    info(f'Bot already disconnected.')
                return
            if requests.post('http://localhost:6969/send', json={"message": msg}).status_code != 200:
                error(f'Failed to send message. (BOT LIKELY NOT CONNECTED)')

    except KeyboardInterrupt: requests.post('http://localhost:6969/disconnect'); return
    except Exception as e: 
        error(e)