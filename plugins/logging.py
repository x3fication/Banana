from colorama import Fore, Style
from plugins.theme import theme

colorz = theme()
white = colorz['white']
yellow = colorz['yellow']
red = colorz['red']
green = colorz['green']
gray = '\033[90m'

from datetime import datetime

class logging:
    @staticmethod
    def format(symbol, color, message, end, flush=False):
        print(f'{white}{datetime.now().strftime("%H:%M")} {gray}[ {color}{symbol} {gray}]{white} {message}', end=end, flush=flush)

    @staticmethod
    def error(message, end="\n", flush=False):
        logging.format('x', red, message, end, flush)

    @staticmethod
    def info(message, end="\n", flush=False):
        logging.format('!', white, message, end, flush)

    @staticmethod
    def success(message, end="\n", flush=False):
        logging.format('+', yellow, message, end, flush)