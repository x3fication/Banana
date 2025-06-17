from mcstatus import JavaServer
from plugins.common import *
import threading
import socket
import string

def chico2(server, save, online_filter, maximum_ping, file, version_filter):
    try:
        lookup = JavaServer.lookup(server)
        status = lookup.status()
        if status.players.online < online_filter or round(status.latency) > maximum_ping: return
        if version_filter is not None and status.version.name != version_filter: return
        if save:
            outputfile = './output/banana.txt' if file is None else './output/{}-travel.txt'.format(str(file).split('.')[0])
            with open(outputfile, 'a+', encoding='UTF-8') as f:
                servers = f.readlines()
                if server not in servers:
                    if version_filter == None: f.write(f'({server})({status.players.online}/{status.players.max})({round(status.latency)}ms)({status.version.name})({status.version.protocol})\n')
                    elif version_filter == status.version.name: f.write(f'({server})({status.players.online}/{status.players.max})({round(status.latency)}ms)({status.version.name})({status.version.protocol})\n')

    except TimeoutError: pass
    except Exception as e: pass


def mcscan2(server, ports, online_filter, maximum_ping ,save=False, file=None, version_filter=None):
    if not checkserver(server): logging.error('Please input a real domain or server'); return

    if '-' in ports: start, end = map(int, ports.split('-'))
    else: start = end = int(ports)

    servers = wow(server)
    if start < 1 or end > 65535: logging.error('Please enter a valid range'); return
    if start > end: logging.error('Start port has to be <= end port'); return
    threads = []

    for srv in servers:
        for port in range(start, end + 1):
            serverz = f'{srv}:{port}'
            t = threading.Thread(target=chico2, args=(serverz, save, online_filter, maximum_ping, file, version_filter), daemon=True)
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

## s tst spmo
def wow(ip12xxx):
    parts = ip12xxx.split('.')
    if len(parts) != 4: return [ip12xxx]

    ranges = []
    for part in parts:
        if part == '*': ranges.append(range(1, 256))
        else: ranges.append([int(part)])

    ips = [f"{i}.{j}.{k}.{l}" for i in ranges[0] for j in ranges[1] for k in ranges[2] for l in ranges[3]]
    return ips

def chico(server):
    try:
        lookup = JavaServer.lookup(server)
        status = lookup.status()
        logging.success(f"{yellow}({white}{server}{yellow})({white}{status.players.online}/{status.players.max}{yellow})({white}{round(status.latency)}ms{yellow})({white}{status.version.name}{yellow})({white}{status.version.protocol}{yellow})")
    except TimeoutError: pass
    except Exception: pass

def mcscan(server, ports, mthreads):
    if not checkserver(server): logging.error('Please input a real domain or server'); return

    if '-' in ports: start, end = map(int, ports.split('-'))
    else: start = end = int(ports)

    servers = wow(server)
    if start < 1 or end > 65535: logging.error('Please enter a valid range'); return
    if start > end: logging.error('Start port has to be <= end port'); return
    threads = []

    for srv in servers:
        for port in range(start, end + 1):
            while threading.active_count() > int(mthreads):
                pass
            serverz = f'{srv}:{port}'
            t = threading.Thread(target=chico, args=(serverz,), daemon=True)
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

def service(port):
    try: return socket.getservbyport(port)
    except Exception: return "unknown"

def tcpping(server, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            if s.connect_ex((server, port)) == 0:
                logging.success(f"{yellow}({white}{server}{yellow})({white}{port}{yellow})({white}{service(port)}{yellow})")

def scan(server, ports, mthreads):
    if not checkip(server): logging.error('Please input a real domain or server'); return
    servers = wow(server)
    if '-' in ports: start, end = map(int, ports.split('-'))
    else: start = end = int(ports)
    if start < 1 or end > 65535: logging.error('Please enter a valid range'); return
    if start > end: logging.error('Start port has to be <= end port'); return
    monkey = []
    for host in servers:
        for port in range(start, end + 1):
            while threading.active_count() > int(mthreads):
                pass
            t = threading.Thread(target=tcpping, args=(host, port))
            t.start()
            monkey.append(t)

    for t in monkey:
        t.join()