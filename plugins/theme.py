import json
from colorama import Fore, Style
from plugins.common import *

THEMES = {
    "banana": {
        "white": '\033[38;2;255;255;255m',
        "yellow": '\033[38;2;255;252;189m',
        "red": Fore.RED + Style.BRIGHT,
        "green": Fore.GREEN + Style.BRIGHT,
    },
    "snow": {
        "white": '\033[38;2;230;230;230m',
        "yellow": '\033[38;2;192;237;249m',
        "red": Fore.LIGHTRED_EX,
        "green": Fore.LIGHTGREEN_EX,
    },
    "sunset": {
        "white": '\033[38;2;235;219;178m',
        "yellow": '\033[38;2;255;189;89m',
        "red": Fore.RED + Style.BRIGHT,
        "green": Fore.YELLOW + Style.BRIGHT,
    },
    "charcoal": {
        "white": '\033[38;2;213;210;221m', 
        "yellow": '\033[38;2;98;114;164m',
        "red": '\033[38;2;255;85;85m',     
        "green": '\033[38;2;80;250;123m',  
    },
    "lily": {
        "white": '\033[38;2;217;224;238m', 
        "yellow": '\033[38;2;245;194;231m',
        "red": '\033[38;2;242;143;173m',   
        "green": '\033[38;2;171;233;179m', 
    }
}

def theme():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        return THEMES["banana"]

    theme_name = str(config['theme']).lower()

    if theme_name not in THEMES:
        theme_name = "banana"

    return THEMES[theme_name]