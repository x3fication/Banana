import threading
import time
import socks
from plugins.common import *
import urllib

zeepa = []
check = 0
lock = threading.Lock()

types = {
    'socks5': socks.SOCKS5,
    'socks4': socks.SOCKS4,
}

sem = threading.Semaphore(50)

def checkproxy(proxy: str):
    global check
    try:
        if '://' not in proxy:
            proxy = 'socks5://' + proxy

        p = urllib.parse.urlparse(proxy)
        scheme = p.scheme.lower()
        host = p.hostname
        port = p.port

        if scheme not in types or host is None or port is None:
            raise ValueError('Invalid proxy string')

        s = socks.socksocket()
        s.set_proxy(types[scheme], host, port, username=p.username, password=p.password)
        s.settimeout(5)
        s.connect(('8.8.8.8', 80))
        s.close()

        with lock:
            zeepa.append(proxy)

    except Exception:
        pass
    finally:
        with lock:
            check += 1
            print(f"\rChecked ({check}) | Good ({len(zeepa)})", end='', flush=True)

def fetch(ptype: str):
    global zeepa, check
    zeepa = []
    check = 0

    # clear old proxies
    with open('proxies.txt', 'w', encoding='utf-8') as f:
        f.write('')

    proxies = scrapeproxy(ptype)
    if not proxies:
        logging.error(f"No {ptype} proxies found")
        return

    threads = []
    for proxy in proxies:
        t = threading.Thread(target=checkproxy, args=(proxy,), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.06)  # delay thread creation

    for t in threads:
        t.join()

    # save valid proxies
    with open('proxies.txt', 'a', encoding='utf-8') as f:
        for proxy in zeepa:
            f.write(f"{proxy}\n")

    print('\n')
    logging.success(f"Saved {len(zeepa)} valid {ptype} proxies")