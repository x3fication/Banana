from plugins.common import *
import requests

def connect(username, server):
    try:
        if checkserver(server) == False: logging.error('Please input a real domain or server'); return
        if ':' in server: gzeht = str(server).split(':'); server = gzeht[0]; port = int(gzeht[1])
        else: port = 25565
        response = requests.post('http://localhost:6969/connect', json={
            "host": server, "port": port, "username": username
        })

        if response.status_code != 200 and response.status_code != 400:
            return logging.error(f'Failed to connect [{response.status_code}]')

        while True:
            r = requests.get('http://localhost:6969/status').json()[server + ':' + str(port)][username]['connected']
            if r: break
            logging.info('Waiting for connection...')
            time.sleep(1)
        
        logging.info(f'Type "exit" to exit. [beta] this is still very shit but it works for sending messages')
        while True:
            msg = input('> ').strip()
            if msg.lower() == "exit":
                if requests.get('http://localhost:6969/status').json()[server + ':' + str(port)][username]['connected']:
                    requests.post('http://localhost:6969/disconnect', json={"host": server, "port": 25565 if not ':' in server else str(port), "username": username})
                    logging.info(f'Bot disconnected.')
                else:
                    logging.info(f'Bot already disconnected.')
                return

            r = requests.post('http://localhost:6969/send', json={"host": server, "port": port, "username": username, "message": msg})
            if r.status_code != 200: logging.error(f'Failed to send message. (BOT is disconnected) [{r.status_code}]'); return

    except KeyboardInterrupt: requests.post('http://localhost:6969/disconnect', json={"host": server, "port": port, "username": username}); return
    except Exception as e: 
        logging.error(e)