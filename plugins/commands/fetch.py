import threading
import socks
from plugins.common import *
import urllib

zeepa = []
check = 0
lock = threading.Lock()

nigga = {
    'socks5': socks.SOCKS5,
    'socks4': socks.SOCKS4,
    'http':   socks.HTTP
}

def checkproxy(proxy: str):
    global check
    try:
        if '://' not in proxy: proxy = 'http://' + proxy
        p = urllib.parse.urlparse(proxy)
        scheme = p.scheme.lower()
        host = p.hostname
        port = p.port
        if scheme not in nigga or host is None or port is None: raise ValueError('Bad proxy string')
        s = socks.socksocket()
        s.set_proxy(nigga[scheme], host, port, username=p.username, password=p.password)
        s.settimeout(5)
        s.connect(('1.1.1.1', 80))
        s.close()
        with lock: zeepa.append(proxy)
    except Exception: pass
    finally:
        with lock:
            check += 1
            print(f"\rcheck ({check}) | Good ({len(zeepa)})", end='', flush=True)

def fetch(ptype):
    with open('proxies.txt', 'w') as f: f.write('') # one ohio one ohio one BIG ohio
    global zeepa, check
    zeepa = []
    check = 0
    proxies = scrapeproxy(ptype)
    threads = []
    for proxy in proxies:
        t = threading.Thread(target=checkproxy, args=(proxy,), daemon=True)
        t.start()
        threads.append(t)

    for t in threads: t.join()
    with open('proxies.txt', 'a+') as f:
        for proxy in zeepa:
            f.write(f'{proxy}\n')
    print('\n')