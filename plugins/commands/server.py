from mcstatus import JavaServer
from plugins.common import *
import socket

def server(server):
    try:
        if ':' in server: x310 = server.split(':'); host = x310[0]; port = x310[1]
        else: host = server
        if checkserver(server) == False: error('Please input a real domain or server'); return
        lookup = JavaServer.lookup(f'{host}:25565' if not ':' in server else f'{host}:{port}')
        status = lookup.status()
    
        print(f"""{yellow}[{white}IP{yellow}]{white} {socket.gethostbyname(server if not ':' in server else server.split(':')[0])}
{yellow}[{white}MOTD{yellow}]{white} {mcparse(status.motd.raw)}
{yellow}[{white}Version{yellow}]{white} {status.version.name}
{yellow}[{white}Protocol{yellow}]{white} {status.version.protocol}
{yellow}[{white}Players{yellow}]{white} {status.players.online}/{status.players.max}
{yellow}[{white}Ping{yellow}]{white} {round(status.latency)}ms""")
    

    except TimeoutError: info('Server is offline')