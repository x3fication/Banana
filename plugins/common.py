import os, re
from colorama import Fore, Style
from plugins.logging import *
import time

white = Fore.WHITE
yellow = Fore.YELLOW + Style.BRIGHT
red = Fore.RED + Style.BRIGHT
green = Fore.GREEN + Style.BRIGHT

clear = lambda: loadmenu(); os.system('cls' if os.name == 'nt' else 'clear')

# Checks if this is the first time that the user loaded banana
def firstload():

    if not os.path.exists("banana"): # Checks if file "banana" exists 
        with open("banana", "w") as f:
            f.write('') # Makes banana file
        return True
    
    # If banana exists will return False
    return False

def animate():
    clear()
    print(f"""
{yellow}      ___                          
     / _ )___ ____  ___ ____  ___ _
    / _  / _ `/ _ \/ _ `/ _ \/ _ `/
   /____/\_,_/_//_/\_,_/_//_/\_,_/ {white}""")
    print("                   ─", end="", flush=True)
    time.sleep(0.1)
    print("\r                  ───", end="", flush=True)
    time.sleep(0.04)
    print("\r                ───────", end="", flush=True)
    time.sleep(0.04)
    print("\r              ───────────", end="", flush=True)
    time.sleep(0.04)
    print("\r           ─────────────────", end="", flush=True)
    time.sleep(0.04)
    print("\r       ─────────────────────────", end="", flush=True)
    time.sleep(0.04)
    print("\r    ────────────────────────────────", end="", flush=True)
    time.sleep(0.04)
    print("\r┣────────────────────────────────────┫", end="", flush=True)
    

# Loads the menu or something
def loadmenu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'''
{yellow}      ___                          
     / _ )___ ____  ___ ____  ___ _
    / _  / _ `/ _ \/ _ `/ _ \/ _ `/
   /____/\_,_/_//_/\_,_/_//_/\_,_/ {white}
┣────────────────────────────────────┫
    {white}Hello {os.getlogin()}. Welcome to {yellow}BANANA
    {white}Type {yellow}help{white} to view the commands
''')

# Checks if server domain is valid with regex
def checkserver(server):

    ipre = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b' # ip regex
    domre = r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$' # domain regex 

    if re.match(domre, server) or re.match(ipre, server):
        return True

    return False