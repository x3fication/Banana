from plugins.common import *
import requests

def kick(username, server):
    try:
        response = requests.post('http://localhost:6969/connect', json={
            "host": server, "port": 25565, "username": username
        })
        if response.status_code != 200 and response.status_code != 400: return error(f'Failed to connect [{response.status_code}]')
        if not requests.get('http://localhost:6969/status').json().get('connected'):
            return error('Bot not connected.')

        while requests.get('http://localhost:6969/status').json().get('connected'):
            time.sleep(3)
            requests.post('http://localhost:6969/disconnect')
        
        info(f'Bot disconnected.')
        success(f'Successfully kicked {username}')
    except Exception as e:
        error(f'{e}')
