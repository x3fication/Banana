import re
import mcstatus
import requests
import string
import socket
import threading
from plugins.common import *
from plugins.commands.scan import mcscan2

limit = threading.Semaphore(50)
found = []
lock = threading.Lock()

# fetch the max page index from minecraftservers.org
def getrange():
    r = requests.get('https://minecraftservers.org/').text
    return max([int(x) for x in re.findall(r'<a href="/index/(.*?)" class="button"', r)]) + 1

# get server status info
def serverdata(server):
    mcstat = mcstatus.JavaServer.lookup(server)
    status = mcstat.status()
    return status.players.online, status.players.max, round(status.latency), status.motd.to_plain(), status.version.name

# check a server against filters and save it
def checks(server, online_filter, maximum_ping, save, filename, version_filter):
    try:
        online, max_players, ping, motd, version = serverdata(server)
        if online < online_filter or ping > maximum_ping:
            return
        if version_filter is not None and version != version_filter:
            return

        with lock:
            if server in found:
                return
            found.append(server)
            print(f"\r{gray}[{yellow}!{gray}] {white}Found {yellow}{len(found)} {white}servers matching your filter.", end="", flush=True)

        if save == 'y':
            clean_motd = motd.replace("\n", "").replace("\r", "")
            entry = f'({server})({online}/{max_players})({ping}ms)({clean_motd})({version})\n'
            with open(f'./output/{filename}', 'a+', encoding='UTF-8') as f:
                f.seek(0)
                if server not in f.read():
                    f.write(entry)

    except Exception:
        pass

# scrape a single page of minecraftservers.org and filter servers
def scrape_page(page, online_filter, maximum_ping, save='y', filename='rizz.txt', version_filter=None, protected_filter='y'):
    try:
        listing = requests.get(f'https://minecraftservers.org/index/{page}').text
        servers = re.findall(r'<div class="url">(.*?)</div>', listing)
        threads = []

        for server in servers:
            try:
                if protected_filter == 'y':
                    ip = socket.gethostbyname(server if ':' not in server else server.split(':')[0])
                    protected = is_protected(ip)
                    if protected not in prots:
                        t = threading.Thread(target=checks, args=(server, online_filter, maximum_ping, save, filename, version_filter), daemon=True)
                        t.start()
                        threads.append(t)
                elif protected_filter == 'n':
                    t = threading.Thread(target=checks, args=(server, online_filter, maximum_ping, save, filename, version_filter), daemon=True)
                    t.start()
                    threads.append(t)
            except Exception:
                pass

        for t in threads:
            t.join()

    except Exception:
        pass

def web():
    try:
        # get filter input
        online_filter = int(input(f'{yellow}Minimum Online ({white}int{yellow})> {white}'))
        maximum_ping = int(input(f'{yellow}Maximum Ping ({white}int{yellow})> {white}'))

        protected_filter = input(f'{yellow}Filter Protected ({white}Ex: TCPShield{yellow}) ({white}y/n{yellow})> {white}')
        if protected_filter not in ['y', 'n']:
            logging.error(f"{red}Please enter a valid value for filter protected{white}")
            return

        filename = input(f'{yellow}File name? ({white}Ex: servers.txt{yellow})> {white}')
        if not str(filename).endswith('.txt'):
            logging.error(f"{red}Please enter a valid filename{white}")
            return

        # travel scan option
        travel = input(f"{yellow}Travel ({white}y/n{yellow})> {white}")
        if travel not in ['y', 'n']:
            logging.error(f"{red}Please enter a valid value for travel{white}")
            return

        if travel == 'y':
            portrange = input(f"{yellow}Port Range? ({white}Ex: 25000-35590 or 25565{yellow})> {white}")
            if '-' in portrange:
                start, end = map(int, portrange.split('-'))
            else:
                start = end = int(portrange)
            if start < 1 or end > 65535:
                logging.error(f"{red}Please enter a valid range{white}")
                return
            if start > end:
                logging.error(f"{red}Start port has to be <= end port{white}")
                return

        # version filter
        dofilterver = input(f"{yellow}Filter Version ({white}y/n{yellow})> {white}")
        if dofilterver not in ['y', 'n']:
            logging.error(f"{red}Please enter a valid value for Filter Version{white}")
            return

        version_filter = input(f"{yellow}Version? ({white}Ex: BungeeCord 1.8.x-1.21.x{yellow})> {white}") if dofilterver == 'y' else None

        # start scraping pages
        maxpage = getrange()
        print(f"{gray}[{yellow}#{gray}] {white}Scraping thru {yellow}{maxpage} {white}indexes")

        scrapingering = []
        for i in range(1, maxpage):
            t = threading.Thread(target=scrape_page, args=(i, online_filter, maximum_ping, 'y', filename, version_filter, protected_filter), daemon=True)
            t.start()
            scrapingering.append(t)

        for t in scrapingering:
            t.join()

        # travel scan for open ports
        if travel == 'y':
            travellingering = []
            print()
            print(f"{gray}[{yellow}#{gray}] {white}Travelling thru {yellow}{len(found)} {white}hosts")
            for s in found:
                try:
                    ip = socket.gethostbyname(s if ':' not in s else s.split(':')[0])
                    t = threading.Thread(target=mcscan2, args=(ip, portrange, online_filter, maximum_ping, True, filename, version_filter), daemon=True)
                    t.start()
                    travellingering.append(t)
                except Exception:
                    pass
            for t in travellingering:
                t.join()

    except Exception as e:
        logging.error(f"{red}Error: {e}{white}")