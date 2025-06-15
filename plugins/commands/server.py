from mcstatus import JavaServer
from plugins.common import *
import socket

def server(server):
    try:
        if checkserver(server) == False: logging.error('Please input a real domain or server'); return
        lookup = JavaServer.lookup(server, timeout=5)
        status = lookup.status()
        ip = lookup.address.resolve_ip()
    
        print(f"""{yellow}[{white}IP{yellow}]{white} {ip} {yellow}({is_protected(ip)})
{yellow}[{white}MOTD{yellow}]{white} {status.motd.to_ansi()}
{yellow}[{white}Version{yellow}]{white} {status.version.name}
{yellow}[{white}Protocol{yellow}]{white} {status.version.protocol}
{yellow}[{white}Players{yellow}]{white} {status.players.online}/{status.players.max}
{yellow}[{white}Ping{yellow}]{white} {round(status.latency)}ms""")
    

    except TimeoutError: logging.info('Server is offline')