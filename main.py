import importlib.util
from plugins.initialize import *
from plugins.common import *
from plugins.logging import *
from plugins.commands.server import server
from plugins.commands.uuid import puuid
from plugins.commands.rcon import rcon
from plugins.commands.rconbrut import rconbrut
from plugins.commands.fuzz import fuzz
from plugins.commands.ipinfo import ipinfo
from plugins.commands.dns import lookup
from plugins.commands.checker import check
from plugins.commands.scan import scan
from plugins.commands.monitor import monitor
from plugins.commands.proxy import proxy
from plugins.commands.connect import connect
from plugins.commands.kick import kick
from plugins.commands.sendcmd import sendcmd
from plugins.commands.shell import shell
from plugins.commands.ogmur import ogmur
from plugins.commands.target import target

scripts = {}

commands = {
    'server': (server, 1, "Usage: server <address>\nShows information about the server"),
    'uuid': (puuid, 1, "Usage: uuid <ign>\nShows player's uuid"),
    'ipinfo': (ipinfo, 1, "Usage: ipinfo <ip>\nShows information about given IP"),
    'monitor': (monitor, 1, "Usage: monitor <ip>\nMonitors who leaves and joins on a specified server (if queries are enabled)"),
    'dns': (lookup, 1, "Usage: dns <domain>\nShows all dns records of domain"),
    'target': (target, 1, "Usage: target <domain>\nShows all subdomains w/ their resolved ips"),
    'proxy': (proxy, 2, "Usage: proxy <ip> <mode>\nStarts a local Velocity proxy server that redirects to the specified server."),
    'check': (check, 1, "Usage: check <file>\nCheck the status of Minecraft servers listed in a specified text file"),
    'scan': (scan, 3, "Usage: scan <ip> <range> <threads>\nCheck the status of Minecraft servers listed in a specified text file\nExample: scan 0.0.0.0 1-65535 10"),
    'clear': (clear, 0, "Clears the screen"),
    'ogmur': (ogmur, 3, "Usage: ogmur <users_file> <server> <commands_file>\nSends a bot that will execute a list of commands from a file"),
    'update': (upd, 0, "Re-Initializes banana"),
    'kick': (kick, 2, "Usage: kick <username> <server>\nKicks a player from the server (if cracked)"),
    'shell': (shell, 1, "Usage: shell <port>\nUses netcat to listen to a port"),
    'connect': (connect, 2, "Usage: connect <username> <server>\nJoins with a bot and allows you to send messages"),
    'rcon': (rcon, 2, "Usage: rcon <server> <password>\nConnects to a server's rcon"),
    'brutrcon': (rconbrut, 2, "Usage: brutrcon <server> <file>\nTries the passwords of the file given to try to connect to rcon"),
    'fuzz': (fuzz, 3, "Usage: fuzz <website> <file> <threads>\nExample: example.com/FUZZ or FUZZ.example.com"),
    'sendcmd': (sendcmd, 3, "Usage: sendcmd <username> <server> <commands_file>\nSends a bot that will execute a list of commands from a file"),
    'exit': (exit, 0, "exit this fuckass app")
}

def chelp(command=None):
    if command is None:
        print(f"{yellow}[{white}Available Commands{yellow}]")
        for cmd, (func, args, msg) in commands.items(): print(f"{yellow}[{white}{cmd}{yellow}] {white}- {msg.splitlines()[0]}")
        for name, script in scripts.items(): print(f"{yellow}[{white}{name}{yellow}] {white}- {script['usage'].splitlines()[0]}")
    elif command in commands:
        _, _, msg = commands[command]
        print(msg)
    elif command in scripts:
        print(scripts[command]['usage'])
    else: print(f'Unknown Command')


def loadscripts(folder='scripts'):
    if not os.path.exists(folder): return
    for filename in os.listdir(folder):
        if filename.endswith('.py'):
            path = os.path.join(folder, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            name = filename[:-3]
            scripts[name] = {
                "module": module,
                "arguments": getattr(module, 'arguments', []),
                "usage": getattr(module, 'usage', ''),
            }

def api():
    gg = os.path.join(os.getcwd(), "api")
    subprocess.Popen(
        ["node", "server.js"],
        cwd=os.path.join(gg),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL
    )

def execmd(cmd):
    try:
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

        elif command in scripts:
            script = scripts[command]
            if len(args) == len(script["arguments"]):
                script["module"].run(dict(zip(script["arguments"], args)))
            else:
                print(script["usage"])

        else: print('Unknown Command')

    except Exception as e: error(e)

if __name__ == '__main__':  
    api()
    initialize() 
    loadscripts()

    while True:
        try:
            cmd = input(f'{white}{os.getlogin()}@{yellow}banana:~{white}$ ')
            execmd(cmd)
        except KeyboardInterrupt: pass
