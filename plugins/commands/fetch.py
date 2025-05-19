import threading
import requests
from plugins.common import *

zeepa = []
check = 0
lock = threading.Lock()

def checkproxy(proxy):
    global check
    proxies = {'http': proxy, 'https': proxy}
    try:
        if requests.get('https://google.com', proxies=proxies, timeout=5).ok:
            with lock: zeepa.append(proxy)
    except: pass
    finally:
        check += 1
        print(f"\r{yellow}Checked ({white}{check}{yellow}) Good ({white}{len(zeepa)}{yellow})", end="", flush=True)

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