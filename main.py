from plugins.initialize import *
from plugins.common import *
from plugins.logging import *
from plugins.commands.server import server
from plugins.commands.uuid import puuid
from plugins.commands.rcon import rcon
from plugins.commands.rconbrut import rconbrut
from plugins.commands.fuzz import fuzz

commands = {
    'server': (server, 1, "Usage: server <address>\nShows information about the server"),
    'uuid': (puuid, 1, "Usage: uuid <ign>\nShows player's uuid"),
    'clear': (clear, 0, "Clears the screen"),
    'update': (upd, 0, "Re-Initializes banana"),
    'rcon': (rcon, 2, "Usage: rcon <server> <password>\nConnects to a server's rcon"),
    'brutrcon': (rconbrut, 2, "Usage: brutrcon <server> <file>\nTries the passwords of the file given to try to connect to rcon"),
    'fuzz': (fuzz, 2, "Usage: fuzz <website> <file>\nExample: example.com/FUZZ or FUZZ.example.com"),
}

def chelp(command=None):
    if command is None:
        print(f"{yellow}[{white}Available Commands{yellow}]")
        for cmd, (func, args, msg) in commands.items(): print(f"{yellow}[{white}{cmd}{yellow}] {white}- {msg.splitlines()[0]}")
    elif command in commands:
        _, _, msg = commands[command]
        print(msg)
    else: print(f'Unknown Command')

def execmd(cmd):
    part = cmd.split()
    if len(part) == 0:
        return
    
    command = part[0]
    args = part[1:]

    if command == "help":
        if len(args) == 0: chelp()
        elif len(args) == 1: chelp(args[0])
    elif command in commands:
        func, required_args, msg = commands[command]
        if len(args) == required_args:
            func(*args)
        else: print(msg)
    else: print('Unknown Command')

if __name__ == '__main__':
    clear()
    initialize()
    while True:
        cmd = input(f'{white}{os.getlogin()}@{yellow}banana:~{white}$ ')
        execmd(cmd)
