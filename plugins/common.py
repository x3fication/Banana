import os
import re
import json
import time
import random
import requests
import threading
from bs4 import BeautifulSoup
from plugins.logging import *
from plugins.theme import theme
from colorama import Fore, Style
import time
import sys

prots = ["TCPShield", 'NeoProtect', 'Cloudflare', "craftserve.pl"]
colorz = theme()
white = colorz['white']
reset = '\033[0m'
yellow = colorz['yellow']
red = colorz['red']
green = colorz['green']
underline = '\033[4m'
hide = "\033[?25l"
show = "\033[?25h"

VERSION = "v0.6"

def ranproxy():
    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    if not proxies:
        return None
    return random.choice(proxies)

def is_protected(host):
    try:
        url = f"http://{host}"
        response = requests.get(url, timeout=5, allow_redirects=False)
        gangster = response.text.lower()
        if 300 <= response.status_code < 400:
            location = response.headers.get("Location")
            if location:
                if "tcpshield" in location: return "TCPShield"
                elif "craftserve.pl" in location: return "craftserve.pl"
                elif "neoprotect" in location: return "NeoProtect"
        
        if "cloudflare" in gangster:
            return "Cloudflare"
        elif "tcpshield" in gangster:
            return "TCPShield"
        elif "craftserve.pl" in gangster:
            return "craftserve.pl"
        elif "neoprotect" in gangster:
            return "NeoProtect"
        else: return 'Unprotected'

    except Exception as e:
        return 'Unprotected'
    
# Checks if this is the first time that the user loaded banana
def firstload():

    if not os.path.exists("banana"): # Checks if file "banana" exists 
        with open("banana", "w") as f:
            f.write('') # Makes banana file
        return True
    
    # If banana exists will return False
    return False

def bananac():
    default = {
        "language": "english",
        "theme": "banana",
        "server": {
            "port": 23457,
            "randomize_port": False
        }
    }

    if not os.path.exists('config.json'):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default, f, indent=2)
        return default

    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    change = False

    if not isinstance(config['server']['port'], int) or not (1 <= config['server']['port'] <= 65535):
        config["server"]["port"] = default["server"]["port"]
        change = True

    if not isinstance(config['server']['randomize_port'], bool):
        config["server"]["randomize_port"] = default["server"]["randomize_port"]
        change = True

    valid_languages = {'jordanian', 'english', 'persian'}
    lang = config['language']
    if lang not in valid_languages:
        config["language"] = default["language"]
        change = True

    if change:
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    return config

import json

def getstring(key):
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    lang = config['language']

    try:
        with open(f"./translations/{lang}.json", 'r', encoding='utf-8') as f:
            strings = json.load(f)
    except FileNotFoundError:
        with open("./translations/english.json", 'r', encoding='utf-8') as f:
            strings = json.load(f)

    return strings.get(key, f"[Missing string for '{key}']")

def animate():
    art = [
        "\n                  ___",
        r"                 / _ )___ ____  ___ ____  ___ _",
        r"                / _  / _ `/ _ \/ _ `/ _ \/ _ `/",
        r"               /____/\_,_/_//_/\_,_/_//_/\_,_/ "
    ]

    w = max(len(line) for line in art)
    shine = 5
    delay = 0.008

    print(hide, end="")
    try:
        for p in range(-shine, w + shine):
            print("\033[H", end="")
            for line in art:
                s = ""
                for i, c in enumerate(line):
                    s += white + c if p <= i < p + shine else yellow + c
                print(s + reset)
            time.sleep(delay)
    finally:
        print(show, end="")
    
def scrapeproxy(ptype):
    if ptype.lower() not in ['socks5', 'socks4']: logging.error('Please enter a valid proxy type (socks5, socks4)'); return
    proxies = []
    try:
        response = requests.get(f'https://raw.githubusercontent.com/RattlesHyper/proxy/main/{ptype}', timeout=5)
        for site in response.text.splitlines():
            r = requests.get(site)
            for proxy in r.text.splitlines():
                proxies.append(f'{ptype}://{proxy}')
        logging.info(f'Fetched {len(proxies)} {ptype} proxies')
        return proxies
    except Exception as e: logging.error(e); return

 
# Loads the menu or something

r"""         _   
       _ \'-_,#
      _\'--','`|
      \`---`  /
       `----'`
"""

def loadmenu():
    print("\033c", end="")
    print(rf'''{yellow}
                  ___                          
                 / _ )___ ____  ___ ____  ___ _        
                / _  / _ `/ _ \/ _ `/ _ \/ _ `/        
               /____/\_,_/_//_/\_,_/_//_/\_,_/ {white} 
''')

import requests
from datetime import datetime

def repostuff():
    repo = "https://api.github.com/repos/x3fication/Banana"
    stars = requests.get(repo).json().get("stargazers_count", 0)
    updated = requests.get(repo).json().get("updated_at")
    return stars, updated, VERSION

def stats(stars, updated, version, width=60):
    if updated:
        updated = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        updated = "N/A"

    def pad(line):
        visible = re.compile(r'\033\[[0-9;]*m').sub('', line)
        return f"{line}{' ' * (width - len(visible) - 1)}{gray}]"

    # print(f'''                {white}Hello {os.getlogin()}. Welcome to {yellow}BANANA{reset}
    #             {white} Type {yellow}help{white} to view commands\n''')
    print(pad(f"       {gray}*[ {yellow}banana {version}{gray}"))
    print(pad(f"+ -- --=[ {white}Stars: {stars}"))
    print(pad(f"{gray}+ -- --=[ {white}Last Updated: {updated}") + '\n')

# Checks if server domain is valid with regex
def checkserver(server):
    if ':' in server:
        server = server.split(':')[0]
    if server == 'localhost': return True
    ipre = r'^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)$'
    domre = r'^(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$'

    if re.match(domre, server) or re.match(ipre, server):
        return True
    return False


def checkip(ip):
    ipre = r'^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)$' # ip regex
    if re.match(ipre, ip): return True
    if '*' in ip: return True
    return False