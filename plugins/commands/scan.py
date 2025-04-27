from mcstatus import JavaServer
from plugins.common import *
import threading

def chico(server):
    try:
        lookup = JavaServer.lookup(server)
        status = lookup.status()
        success(f"{yellow}({white}{server}{yellow})({white}{status.players.online}/{status.players.max}{yellow})({white}{round(status.latency)}ms{yellow})({white}{status.version.name}{yellow})({white}{status.version.protocol}{yellow})")
    except TimeoutError: pass
    except Exception: pass

def scan(server, ports, mthreads):
    ohio = 0
    if checkserver(server) == False: error('Please input a real domain or server'); return
    ports = ports.split('-')
    start = int(ports[0])
    end = int(ports[1])
    if start < 1 or end > 65535: error('Please enter a valid range'); return
    if start > end: error('Start port has to be <= end port'); return
    threads = []
    for port in range(start, end + 1):
        while threading.active_count() > int(mthreads):
            pass
        serverz = f'{server}:{port}'
        t = threading.Thread(target=chico, args=(serverz,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
