from plugins.common import *
import requests
import time

def ogmur(userfile, server, cmdfile, keep, proxy=None):
    try:
        connected = False

        # validate server
        if not checkserver(server):
            logging.error('Please input a real domain or server')
            return

        # validate keep
        elif keep not in ['true', 'false']:
            logging.error('Please enter a valid value: true/false')
            return

        if ':' in server:
            server, port = str(server).split(':')
        else:
            port = 25565

        # read usernames from file
        with open(userfile, 'r') as users_file:
            usernames = [line.strip() for line in users_file if line.strip()]

        # iterate over each username
        for username in usernames:
            payload = {"host": server, "port": port, "username": username}
            if proxy is not None:
                payload["proxy"] = ranproxy()

            logging.info(f'Connecting, {username}')

            # attempt connection
            response = requests.post('http://localhost:6969/connect', json=payload)

            if response.status_code not in [200, 400]:
                return logging.error(f'Failed to connect [{response.status_code}]')

            # wait for connection
            for i in range(10):
                r = requests.get('http://localhost:6969/status').json()[f"{server}:{port}"][username]['connected']
                if r:
                    connected = True
                    break
                logging.info('Waiting for connection...')
                time.sleep(2)

            logging.success(f'Connected {username}')

            # read commands from file
            with open(cmdfile, 'r') as commands_file:
                commands = [line.strip() for line in commands_file if line.strip()]

            # send commands
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

                # disconnect if keep is false
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
