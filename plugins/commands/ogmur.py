from plugins.common import *
import requests
import time

def ogmur(userfile, server, cmdfile, keep, proxy=None):
    try:
        connected = False
        if not checkserver(server):
            logging.error('Please input a real domain or server')
            return

        elif keep not in ['true', 'false']: logging.error('Please enter a valid value: yes/no'); return

        if ':' in server: server, port = str(server).split(':');
        else: port = 25565
        with open(userfile, 'r') as users_file:
            usernames = [line.strip() for line in users_file if line.strip()]

        for username in usernames:
            payload = {"host": server, "port": port, "username": username}
            if proxy is not None: payload["proxy"] = ranproxy()
            logging.info(f'Connecting, {username}')
            response = requests.post('http://localhost:6969/connect', json=payload)

            if response.status_code != 200 and response.status_code != 400:
                return logging.error(f'Failed to connect [{response.status_code}]')

            for i in range(10):
                r = requests.get('http://localhost:6969/status').json()[server + ':' + str(port)][username]['connected']
                if r == True: connected = True;break
                logging.info('Waiting for connection...')
                time.sleep(2)

            logging.success(f'Connected {username}')

            with open(cmdfile, 'r') as commands_file:
                commands = [line.strip() for line in commands_file if line.strip()]

            if connected:
                for command in commands:
                    r = requests.post('http://localhost:6969/send', json={
                        "host": server,
                        "port": port,
                        "username": username,
                        "message": command
                    })
                    if r.status_code != 200:
                        logging.error(f'Failed to send message. (BOT LIKELY DISCONNECTED) {r.status_code}')
                        return

                    logging.success(f'Sent: {command}')
                    time.sleep(0.5)

                logging.success(f'All commands have been sent for {username}')
                if keep == 'false':
                    requests.post('http://localhost:6969/disconnect', json={
                        "host": server,
                        "port": port,
                        "username": username
                    })
                    logging.success(f'{username} has been disconnected')
                time.sleep(3)

    except Exception as e:
        logging.error(e)
