import re
import mcstatus
import requests
import string
import socket
from plugins.common import *
from plugins.commands.scan import mcscan2

limit = threading.Semaphore(50)
found = []
lock = threading.Lock()

def getrange():
    r = requests.get('https://minecraftservers.org/').text
    return max([int(x) for x in re.findall(r'<a href="/index/(.*?)" class="button"', r)]) + 1

def serverdata(server):
    mcstat = mcstatus.JavaServer.lookup(server)
    status = mcstat.status()
    return status.players.online, status.players.max, round(status.latency), status.motd.to_plain(), status.version.name

def checks(server, online_filter, maximum_ping, save, filename):
    try:
        online, max_players, ping, motd, version = serverdata(server)
        print(f"\rFound {len(found)} servers matching your filter.", end="", flush=True)
        if online >= online_filter and ping <= maximum_ping:
            with lock:
                if server not in found:
                    found.append(server)
            if save == 'y':
                with open(fr'./output/{filename}', 'a+', encoding='UTF-8') as f:
                    f.seek(0)
                    servers = f.readlines()
                    if server not in servers:
                        # fuck you nigga python 3.11
                        nl = '\n'
                        cr = '\r'
                        f.write(f'({server})({online}/{max_players})({ping}ms)({motd.replace(nl, "").replace(cr, "")})({version})\n')
    except Exception:
        pass


def scrape_page(page, online_filter, maximum_ping, save, filename):
    try:
        listing = requests.get(f'https://minecraftservers.org/index/{page}').text
        servers = re.findall(r'<div class="url">(.*?)</div>', listing)
        threads = []
        for server in servers:
            try:
                if not is_protected(socket.gethostbyname(server)) in prots:
                    t = threading.Thread(target=checks, args=(server, online_filter, maximum_ping, save, filename), daemon=True)
                    t.start()
                    threads.append(t)
            except Exception:
                pass
        for t in threads:
            t.join()
    except Exception:
        pass


def web():
    online_filter = int(input(f'{yellow}Minimum Online ({white}int{yellow})> '))
    maximum_ping = int(input(f'{yellow}Maximum Ping ({white}int{yellow})> '))
    save = input(f'{yellow}Save to file? ({white}y/n{yellow})> ')
    filename = input(f'{yellow}File name? ({white}Ex: ohio.txt{yellow})> ') if save.lower() == 'y' else None

    travel = input(f"{yellow}Travel ({white}y/n{yellow})> ").lower()
    portrange = input(f"{yellow}Port Range? ({white}Ex: 25000-35590{yellow})> ") if travel == 'y' else None

    maxpage = getrange()
    logging.info(f'Scraping thru {maxpage} indexes')

    scrapingering = []
    for i in range(1, maxpage):
        t = threading.Thread(target=scrape_page, args=(i, online_filter, maximum_ping, save, filename), daemon=True)
        t.start()
        scrapingering.append(t)

    for t in scrapingering:
        t.join()

    if travel == 'y':
        travellingering = []
        print(f'')
        print(f'Travelling thru {len(found)} hosts')
        for s in found:
            try:
                ip = socket.gethostbyname(s)
                t = threading.Thread(target=mcscan2, args=(ip, portrange, 5, True, filename), daemon=True)
                t.start()
                travellingering.append(t)
            except Exception:
                pass
        for t in travellingering:
            t.join()