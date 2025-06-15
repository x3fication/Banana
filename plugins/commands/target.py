import requests
from plugins.common import *

def target(domain):
    if checkserver(domain) == False: logging.error('Please input a real domain'); return

    r = requests.get(f'https://api.hackertarget.com/hostsearch/?q={domain}')
    results = r.text.strip().split('\n')
    for result in results:
        ohio = result.split(',')
        logging.success(f'{white}{ohio[0].ljust(50)} {yellow}{white}{ohio[1]}{yellow} ({is_protected(ohio[1])})')