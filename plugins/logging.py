from colorama import Fore, Style

white = Fore.WHITE
yellow = Fore.YELLOW + Style.BRIGHT
red = Fore.RED + Style.BRIGHT
green = Fore.GREEN + Style.BRIGHT

def format(symbol, color, message):
    print(f'{yellow}[ {color}{symbol} {yellow}] {message}')

def error(message):
    format('x', red, message)

def info(message):
    format('!', white, message)

def success(message):
    format('+', green, message)
