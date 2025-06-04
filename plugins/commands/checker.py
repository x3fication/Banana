from mcstatus import JavaServer
from plugins.common import *

def check(file):
    with open(file, 'r') as f:
             servers = [line.strip() for line in f if line.strip()]
    for server in servers:
        try:
                lookup = JavaServer.lookup(server)
                status = lookup.status()
                logging.success(f"{yellow}({white}{server}{yellow})({white}{status.players.online}/{status.players.max}{yellow})({white}{round(status.latency)}ms{yellow})({white}{status.version.name}{yellow})({white}{status.version.protocol}{yellow})")
        except TimeoutError: pass
        except Exception: pass