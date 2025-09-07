from mcstatus import JavaServer
from plugins.common import *
import socket

# check server status using mcstatus
def server(server):
    try:
        # validate server input
        if not checkserver(server):
            logging.error('Please input a real domain or server')
            return

        # fetch server status and IP
        lookup = JavaServer.lookup(server, timeout=5)
        status = lookup.status()
        ip = lookup.address.resolve_ip()

        print(f"\n{gray}[{yellow}#{gray}] {white}Checking {yellow}{server}{white} via {gray}mcstatus{white}...\n")
        print(f"{white}• {yellow}IP:{white} {ip} {yellow}({is_protected(ip)})")

        print(f"{white}• {yellow}MOTD:{white}")
        motd = status.motd.to_ansi().splitlines()
        for line in motd:
            print(f"  {gray}•{white} {line}")

        print(f"{white}• {yellow}Version:{white} {status.version.name}")
        print(f"{white}• {yellow}Protocol:{white} {status.version.protocol}")
        print(f"{white}• {yellow}Players:{white} {status.players.online}/{status.players.max}")
        print(f"{white}• {yellow}Ping:{white} {round(status.latency)}ms\n")

    except TimeoutError: logging.info('Server is offline')
