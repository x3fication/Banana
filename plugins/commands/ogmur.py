from plugins.common import *
import requests
import time

def ogmur(userfile, server, cmdfile, keep):
    try:
        if not checkserver(server):
            error('Please input a real domain or server')
            return

        elif keep not in ['true', 'false']: error('Please enter a valid value: yes/no'); return

        if ':' in server:
            dorize = server.split(':')
            server = dorize[0]
            port = int(dorize[1])
        else:
            port = 25565
        with open(userfile, 'r') as users_file:
            usernames = [line.strip() for line in users_file if line.strip()]

        for username in usernames:
            info(f'Connecting, {username}')
            response = requests.post('http://localhost:6969/connect', json={
                "host": server,
                "port": port,
                "username": username
            })

            if response.status_code != 200 and response.status_code != 400:
                return error(f'Failed to connect [{response.status_code}]')

            server_key = f"{server}:{port}"
            while True:
                r = requests.get('http://localhost:6969/status').json()[server + ':' + str(port)][username]['connected']
                if r == True: break
                info('Waiting for connection...')
                time.sleep(1)

            success(f'Connected {username}')

            with open(cmdfile, 'r') as commands_file:
                commands = [line.strip() for line in commands_file if line.strip()]

            for command in commands:
                r = requests.post('http://localhost:6969/send', json={
                    "host": server,
                    "port": port,
                    "username": username,
                    "message": command
                })
                if r.status_code != 200:
                    error(f'Failed to send message. (BOT LIKELY DISCONNECTED) {r.status_code}')
                    return

                success(f'Sent: {command}')
                time.sleep(0.5)

            success(f'All commands have been sent for {username}')
            if keep == 'false':
                requests.post('http://localhost:6969/disconnect', json={
                    "host": server,
                    "port": port,
                    "username": username
                })
                success(f'{username} has been disconnected')
            time.sleep(3)

    except Exception as e:
        error(e)
