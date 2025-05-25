from plugins.common import *
import requests

def kick(username, server, proxy=None):
    try:
        connected = False
        if checkserver(server) == False: logging.error('Please input a real domain or server'); return
        if ':' in server: server, port = str(server).split(':');
        else: port = 25565
        
        payload = {"host": server, "port": port, "username": username}
        if proxy is not None: payload["proxy"] = ranproxy()
        response = requests.post('http://localhost:6969/connect', json=payload)
        if response.status_code != 200: return logging.error(f'Failed to connect [{response.status_code}]')
        for i in range(10):
            r = requests.get('http://localhost:6969/status').json()[server + ':' + str(port)][username]['connected']
            if r == True: connected = True; break
            logging.info('Waiting for connection...')
            time.sleep(2)
        
        if connected: requests.post('http://localhost:6969/disconnect', json={"host": server, "port": port, "username": username}); logging.info(f'Bot disconnected.'); logging.success(f'Successfully kicked {username}')

    except Exception as e:
        logging.error(f'{e}')
