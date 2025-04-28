from plugins.common import *
import requests
import time

def sendcmd(username, server, file):
    try:
        response = requests.post('http://localhost:6969/connect', json={
            "host": server, "port": 25565, "username": username
        })
        if response.status_code != 200 and response.status_code != 400:
            return error(f'Failed to connect [{response.status_code}]')

        while not requests.get('http://localhost:6969/status').json().get('connected'):
            pass
        
        with open(file, 'r') as f:
            commands = [line.strip() for line in f if line.strip()] 
        
        for command in commands:
            if requests.post('http://localhost:6969/send', json={"message": command}).status_code != 200:
                error(f'Failed to send message. (BOT LIKELY NOT CONNECTED)')
            success(f'Sent {command}')
            time.sleep(0.5)

        success(f'All commands have been sent')

    except Exception as e:
        error(e)
