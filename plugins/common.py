import os
import re
import json
import time
import random
import requests
import threading
from plugins.logging import *
from plugins.theme import theme
from colorama import Fore, Style
from plugins.minecolor import mcparse



colorz = theme()
white = colorz['white']
reset = '\033[0m'
yellow = colorz['yellow']
red = colorz['red']
green = colorz['green']
underline = '\033[4m'

clear = lambda: loadmenu(); print("\033c", end="")

def ranproxy():
    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    if not proxies:
        return None
    return random.choice(proxies)


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
    lang = config['language']['english']
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
    print("\033c", end="")
    print(rf"""
{yellow}      ___                          
     / _ )___ ____  ___ ____  ___ _
    / _  / _ `/ _ \/ _ `/ _ \/ _ `/
   /____/\_,_/_//_/\_,_/_//_/\_,_/ {white}""")

    for i in range(19):
        line = "─" * i
        space = " " * (19 - i)
        print("\r" + space + line * 2, end="", flush=True)
        time.sleep(0.03)
    
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
    print(rf'''
{yellow}      ___                          
     / _ )___ ____  ___ ____  ___ _        
    / _  / _ `/ _ \/ _ `/ _ \/ _ `/        
   /____/\_,_/_//_/\_,_/_//_/\_,_/ {white} 
┣────────────────────────────────────┫
    {white}Hello {os.getlogin()}. Welcome to {yellow}BANANA{reset}
    {white}Type {yellow}help{white} to view the commands
''')

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