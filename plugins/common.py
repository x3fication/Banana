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
import requests
from datetime import datetime

prots = ["TCPShield", 'NeoProtect', 'Cloudflare', "craftserve.pl"]
colorz = theme()
white = colorz['white']
yellow = colorz['yellow']
red = colorz['red']
green = colorz['green']
underline = '\033[4m'
hide = "\033[?25l"
show = "\033[?25h"
reset = '\033[0m'

VERSION = "v0.6"

IP_REGEX = r'^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)\.((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)|\*)$'
DOM_REGEX = r'^(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$'


def firstload():
    return not os.path.exists("banana")

def ranproxy():
    try:
        with open('proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        return random.choice(proxies) if proxies else None
    
    except Exception:
        return None

def is_protected(host):
    protections = {
        "cloudflare": "Cloudflare",
        "tcpshield": "TCPShield",
        "craftserve.pl": "craftserve.pl",
        "neoprotect": "Neoprotect"
    }
    try:
        url = f"http://{host}"
        response = requests.get(url, timeout=5, allow_redirects=False)
        content = response.text.lower()

        # check if redirected
        if 300 <= response.status_code < 400:
            location = response.headers.get("Location")
            if location:
                if "tcpshield" in location: return "TCPShield"
                elif "craftserve.pl" in location: return "craftserve.pl"
                elif "neoprotect" in location: return "NeoProtect"
        
        # check page content
        for prot, name in protections.items():
            if prot in content:
                return name

        return "Unprotected"

    except Exception as e:
        return "Unprotected"

def bananac():
    default = {
        "language": "english",
        "theme": "banana",
        "server": {
            "port": 23457,
            "randomize_port": False
        }
    }

    # create config if doesn't exist
    if not os.path.exists('config.json'):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default, f, indent=2)
        return default

    # load config
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    change = False

    # validation for port
    if not isinstance(config['server']['port'], int) or not (1 <= config['server']['port'] <= 65535):
        config["server"]["port"] = default["server"]["port"]
        change = True

    # validation for random port
    if not isinstance(config['server']['randomize_port'], bool):
        config["server"]["randomize_port"] = default["server"]["randomize_port"]
        change = True

    # validation for languages
    valid_languages = {'jordanian', 'english', 'persian'}
    lang = config['language']
    if lang not in valid_languages:
        config["language"] = default["language"]
        change = True

    # save if values changed
    if change: 
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    return config

def getstring(key):
    # load config
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # get language from config | default to english
    lang = config.get("language", "english")

    try:
        # load translation for language
        with open(f"./translations/{lang}.json", 'r', encoding='utf-8') as f:
            strings = json.load(f)

    except FileNotFoundError:
        # fallback to english if language doesnt exist
        with open("./translations/english.json", 'r', encoding='utf-8') as f:
            strings = json.load(f)

    # return string for key if missing
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
    proxies = []

    # validate proxy type
    if ptype.lower() not in ['socks5', 'socks4']:
        logging.error('Please enter a valid proxy type (socks5, socks4)')
        return
    
    try:
        # fetch proxy sites
        response = requests.get(f'https://raw.githubusercontent.com/RattlesHyper/proxy/main/{ptype}', timeout=5)

        for site in response.text.splitlines():
            r = requests.get(site)
            # add every proxy to "proxies" list
            for proxy in r.text.splitlines():
                proxies.append(f'{ptype}://{proxy}')

        # log numbers of proxies found
        logging.info(f'Fetched {len(proxies)} {ptype} proxies')
        return proxies
    
    except Exception as e:
        logging.error(e)
        return

def loadmenu():
    print("\033c", end="")
    print(rf'''{yellow}
                  ___                          
                 / _ )___ ____  ___ ____  ___ _        
                / _  / _ `/ _ \/ _ `/ _ \/ _ `/        
               /____/\_,_/_//_/\_,_/_//_/\_,_/ {white} 
''')


def repostuff():
    repo = "https://api.github.com/repos/x3fication/Banana"
    r = requests.get(repo).json()
    stars = r["stargazers_count"]
    updated = r["updated_at"]
    return stars, updated, VERSION

def stats(stars, updated, version, width=60):
    if updated:
        updated = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        updated = "N/A"

    def pad(line):
        visible = re.compile(r'\033\[[0-9;]*m').sub('', line)
        return f"{line}{' ' * (width - len(visible) - 1)}{gray}]"

    print(pad(f"       {gray}*[ {yellow}banana {version}{gray}"))
    print(pad(f"+ -- --=[ {white}Stars: {stars}"))
    print(pad(f"{gray}+ -- --=[ {white}Last Updated: {updated}") + '\n')


def checkserver(server):
    server = server.split(':')[0]
    if server == 'localhost': return True
    return bool(re.match(DOM_REGEX,server) or re.match(IP_REGEX, server))


def checkip(ip):
    return bool(re.match(IP_REGEX, ip) or '*' in ip)