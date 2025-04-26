from mcrcon import MCRcon
from plugins.common import *

def rcon(server, password):
    try:
        print(f'{yellow}[ ! ] Type "exit" to exit the rcon client')
        with MCRcon(server, password) as mcr:
            while True:
               rcmd = input(f'{yellow}/')
               if rcmd == 'exit': mcr.disconnect(); return False
               resp = mcr.command(f"/{rcmd}")
               print(resp)

    except Exception as e:
        print(e)