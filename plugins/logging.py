from colorama import Fore, Style

white = Fore.WHITE
yellow = Fore.YELLOW + Style.BRIGHT
red = Fore.RED + Style.BRIGHT
green = Fore.GREEN + Style.BRIGHT

from datetime import datetime

class logging:
    @staticmethod
    def format(symbol, color, message, end, flush=False):
        print(f'{yellow}{white}{datetime.now().strftime("%H:%M")} {yellow}[ {color}{symbol} {yellow}] {message}', end=end, flush=flush)

    @staticmethod
    def error(message, end="\n", flush=False):
        logging.format('x', red, message, end, flush)

    @staticmethod
    def info(message, end="\n", flush=False):
        logging.format('!', white, message, end, flush)

    @staticmethod
    def success(message, end="\n", flush=False):
        logging.format('+', green, message, end, flush)