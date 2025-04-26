from mcstatus import JavaServer
from plugins.common import *
import socket

def server(server):
    try:
        check = checkserver(server)
        if check == True:
            lookup = JavaServer.lookup(server)
            status = lookup.status()
    
            print(f"""{yellow}[{white}IP{yellow}]{white} {socket.gethostbyname(server)}
{yellow}[{white}MOTD{yellow}]{white} {status.motd.raw}
{yellow}[{white}Version{yellow}]{white} {status.version.name}
{yellow}[{white}Protocol{yellow}]{white} {status.version.protocol}
{yellow}[{white}Players{yellow}]{white} {status.players.online}/{status.players.max}
{yellow}[{white}Ping{yellow}]{white} {round(status.latency)}ms""")
    
        elif check == False: error('Please input a real domain or server')

    except TimeoutError: info('Server is offline')