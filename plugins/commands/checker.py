from mcstatus import JavaServer
from plugins.common import *

def check(file):
    # load server list from file
    with open(file, 'r') as f:
             servers = [line.strip() for line in f if line.strip()]

    # check each server
    for server in servers:
        try:
                lookup = JavaServer.lookup(server)
                status = lookup.status()
                logging.success(
                    f"{yellow}({white}{server}{yellow})"
                    f"({white}{status.players.online}/{status.players.max}{yellow})"
                    f"({white}{round(status.latency)}ms{yellow})"
                    f"({white}{status.version.name}{yellow})"
                    f"({white}{status.version.protocol}{yellow})"
            )
    
        # skip bullshit
        except TimeoutError: pass
        except Exception: pass