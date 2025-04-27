from mcrcon import MCRcon
from plugins.common import *

def rcon(server, password):
    if checkserver(server) == False: error('Please input a real domain or server'); return
    try:
        with MCRcon(server, password) as mcr:
            print(f'{yellow}[ ! ] Type "exit" to exit the rcon client')
            while True:
               rcmd = input(f'{yellow}/')
               if rcmd == 'exit': mcr.disconnect(); return False
               resp = mcr.command(f"/{rcmd}")
               print(resp)

    except Exception as e:
        print(e)