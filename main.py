import threading
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
from plugins.commands.scan import mcscan
from plugins.commands.scan import scan
from plugins.commands.monitor import monitor
from plugins.commands.proxy import proxy
from plugins.commands.connect import connect
from plugins.commands.kick import kick
from plugins.commands.sendcmd import sendcmd
from plugins.commands.shell import shell
from plugins.commands.ogmur import ogmur
from plugins.commands.target import target
from plugins.commands.fakeproxy import fakeproxy
from plugins.commands.fetch import fetch
from plugins.commands.edit import edit
from plugins.commands.bungeeguard import bungee
from plugins.commands.websearch import web
from plugins.commands.pterodactyl import ptero
from plugins.commands.iphistory import iphistory


scripts = {}

"""
    if u want to add ur own commands do here is the format
        (func, required_args, optional_args, usage)
"""

stars, updated, version = repostuff()
clear = lambda: loadmenu(); print("\033c", end="")

def flush():
    print("\033c", end="")
    loadmenu()
    stats(stars, updated, version)

def getcmds():
    return {
        'iphistory':    (iphistory, 1, 0, getstring('iphistoryh')),
        'websearch':    (web, 0, 0, getstring('websearchh')),
        'server':       (server, 1, 0, getstring('serverh')),
        'edit':         (edit, 1, 1, getstring('edith')),
        'bungeeguard':  (bungee, 2, 0, getstring('bungeeguardh')),
        'ptero':        (ptero, 1, 0, getstring('pteroh')),
        'uuid':         (puuid, 1, 0, getstring('uuidh')),
        'ipinfo':       (ipinfo, 1, 0, getstring('ipinfoh')),
        'fetch':        (fetch, 1, 0, getstring('fetchh')),
        'monitor':      (monitor, 1, 0, getstring('monitorh')),
        'dns':          (lookup, 1, 0, getstring('dnsh')),
        'target':       (target, 1, 0, getstring('targeth')),
        'proxy':        (proxy, 2, 0, getstring('proxyh')),
        'fakeproxy':    (fakeproxy, 2, 0, getstring('fakeproxyh')),
        'check':        (check, 1, 0, getstring('checkh')),
        'mcscan':       (mcscan, 3, 0, getstring('mcscanh')),
        'scan':         (scan, 3, 0, getstring('scanh')),
        'clear':        (flush, 0, 0, getstring('clearh')),
        'ogmur':        (ogmur, 4, 1, getstring('ogmurh')),
        'update':       (upd, 0, 0, getstring('updateh')),
        'kick':         (kick, 2, 1, getstring('kickh')),
        'shell':        (shell, 3, 0, getstring('shellh')),
        'connect':      (connect, 2, 1, getstring('connecth')),
        'rcon':         (rcon, 2, 0, getstring('rconh')),
        'brutrcon':     (rconbrut, 2, 0, getstring('brutrconh')),
        'fuzz':         (fuzz, 3, 0, getstring('fuzzh')),
        'sendcmd':      (sendcmd, 3, 1, getstring('sendcmdh')),
        'exit':         (exit, 0, 0, getstring('exith'))
    }

def chelp(command=None):
    commands = getcmds()

    if command is None:
        entries = []
        for cmd, entry in sorted(commands.items()):
            msg = entry[2] if len(entry) == 3 else entry[3]
            lines = msg.strip().splitlines()
            desc = lines[1] if len(lines) > 1 else lines[0]
            entries.append((cmd, desc))

        maxcmd = max(len(cmd) for cmd, _ in entries)
        desclen = max(len(desc) for _, desc in entries)
        width = maxcmd + desclen + 7

        print(f"{white}{' Available Commands '.center(width)}")
        print(f"{gray}┌{'─' * (maxcmd + 2)}┬{'─' * (desclen + 2)}┐")
        print(f"{gray}│ {yellow}{'Command'.ljust(maxcmd)} {gray}│ {white}{'Description'.ljust(desclen)} {gray}│")
        print(f"{gray}├{'─' * (maxcmd + 2)}┼{'─' * (desclen + 2)}┤")

        for cmd, desc in entries:
            print(f"{gray}│ {yellow}{cmd.ljust(maxcmd)} {gray}│ {white}{desc.ljust(desclen)} {gray}│")

        print(f"{gray}└{'─' * (maxcmd + 2)}┴{'─' * (desclen + 2)}┘\n")

    elif command in commands:
        msg = commands[command][2] if len(commands[command]) == 3 else commands[command][3]
        print(msg)

    elif command in scripts:
        print(scripts[command]['usage'])

    else:
        print('Unknown command')

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
    subprocess.run(fr'"C:\Program Files/nodejs/node.exe" server.mjs' if os.name == 'nt' else 'node server.mjs',
        cwd=os.path.join(gg),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        shell=True
    )

def execmd(cmd):
    commands = getcmds()
    try:
        part = cmd.split()
        if len(part) == 0: return
        command, *args = part
        if command == "help":
            chelp(args[0] if args else None)
            return
        if command in commands:
            func, required_args, *rest = commands[command]
            optional_args = 0
            usage = ''
            if rest:
                if len(rest) == 2:
                    optional_args, usage = rest
                else:
                    usage = rest[0]
            if required_args <= len(args) <= required_args + optional_args:
                func(*args)
            else:
                print(usage)
            return
        if command in scripts:
            script = scripts[command]
            if len(args) == len(script["arguments"]):
                script["module"].run(dict(zip(script["arguments"], args)))
            else:
                print(script["usage"])
            return
        print('Unknown Command')
    except Exception as e:
        logging.error(e)


    except Exception as e: logging.error(e)

if __name__ == '__main__':
    initialize()
    threading.Thread(target=api, daemon=True).start()
    loadscripts()
    stats(stars, updated, version)

    while True:
        try:
            cmd = input(f'{underline}{yellow}banana{reset} > ')
            execmd(cmd)
        except KeyboardInterrupt: pass
        except EOFError: pass