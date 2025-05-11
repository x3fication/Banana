import os, re, json
from colorama import Fore, Style
from plugins.logging import *
import time
from plugins.minecolor import mcparse

white = '\033[38;2;255;255;255m'
reset = '\033[0m'
yellow = '\033[38;2;255;252;189m'
bgyellow = '\033[48;2;255;252;189m'
red = Fore.RED + Style.BRIGHT
green = Fore.GREEN + Style.BRIGHT
underline = '\033[4m'

clear = lambda: loadmenu(); print("\033c", end="")

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
        "server": {
            "port": 23457,
            "randomize_port": False
        }
    }

    if not os.path.exists('config.json'):
        with open('config.json', 'w') as f:
            json.dump(default, f, indent=2)
        return default

    with open('config.json', 'r') as f:
        config = json.load(f)

    change = False

    if not isinstance(config['server']['port'], int) or not (1 <= config['server']['port'] <= 65535):
        config["server"]["port"] = default["server"]["port"]
        change = True

    if not isinstance(config['server']['randomize_port'], bool):
        config["server"]["randomize_port"] = default["server"]["randomize_port"]
        change = True

    if change:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)

    return config

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
    ipre = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    domre = r'^(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$'

    if re.match(domre, server) or re.match(ipre, server):
        return True
    return False


def checkip(ip):
    ipre = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b' # ip regex
    if re.match(ipre, ip):
        return True

    return False