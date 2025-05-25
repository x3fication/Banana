from plugins.common import *
import requests
import time

def sendcmd(username, server, file, proxy=None):
    try:
        connected = False
        if checkserver(server) == False: logging.error('Please input a real domain or server'); return
        if ':' in server: server, port = str(server).split(':');
        else: port = 25565
        logging.info('Connecting..')
        payload = {"host": server, "port": port, "username": username}
        if proxy is not None: payload["proxy"] = ranproxy()
        print(payload)
        response = requests.post('http://localhost:6969/connect', json=payload)
        if response.status_code != 200 and response.status_code != 400:
            return logging.error(f'Failed to connect [{response.status_code}]')
        for i in range(10):
            r = requests.get('http://localhost:6969/status').json()[server + ':' + str(port)][username]['connected']
            if r == True: connected = True; break
            logging.info('Waiting for connection...')
            time.sleep(2)
        
        with open(file, 'r') as f:
            commands = [line.strip() for line in f if line.strip()] 
        
        if connected:
            logging.success('Connected')
            for command in commands:
                
                r = requests.post('http://localhost:6969/send', json={"host": server, "port": port, "username": username, "message": command})
                if r.status_code != 200:
                    logging.error(f'Failed to send message. (BOT LIKELY DISCONNECTED) {r.status_code}')
                    return

                logging.success(f'Sent {command}')
                time.sleep(0.5)

            logging.success(f'All commands have been sent')
            requests.post('http://localhost:6969/disconnect', json={"host": server, "port": port, "username": username})
    except Exception as e:
        logging.error(e)
