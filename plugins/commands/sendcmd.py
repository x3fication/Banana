from plugins.common import *
import requests
import time

def sendcmd(username, server, file):
    try:
        if checkserver(server) == False: logging.error('Please input a real domain or server'); return
        if ':' in server: gzeht = str(server).split(':'); server = gzeht[0]; port = int(gzeht[1])
        else: port = 25565
        logging.info('Connecting..')
        response = requests.post('http://localhost:6969/connect', json={
            "host": server, "port": port, "username": username
        })
        if response.status_code != 200 and response.status_code != 400:
            return logging.error(f'Failed to connect [{response.status_code}]')
        logging.success('Connected')
        while True:
            r = requests.get('http://localhost:6969/status').json()[server + ':' + str(port)][username]['connected']
            if r == True: break
            logging.info('Waiting for connection...')
            time.sleep(1)
        
        with open(file, 'r') as f:
            commands = [line.strip() for line in f if line.strip()] 
        
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
