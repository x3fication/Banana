from plugins.common import *
import requests

def kick(username, server):
    try:
        if checkserver(server) == False: error('Please input a real domain or server'); return
        if ':' in server: gzeht = str(server).split(':'); server = gzeht[0]; port = int(gzeht[1])
        else: port = 25565

        response = requests.post('http://localhost:6969/connect', json={
            "host": server, "port": port, "username": username
        })
        if response.status_code != 200: return error(f'Failed to connect [{response.status_code}]')
        while True:
            r = requests.get('http://localhost:6969/status').json()[server + ':' + str(port)][username]['connected']
            if r == True: break
            info('Waiting for connection...')
            time.sleep(1)
            
        requests.post('http://localhost:6969/disconnect', json={"host": server, "port": 25565 if not ':' in server else port, "username": username})
        
        info(f'Bot disconnected.')
        success(f'Successfully kicked {username}')
    except Exception as e:
        error(f'{e}')
