from plugins.common import *

def scrapetype(type):
    dorito = []
    proxies = scrapeproxy(type)
    logging.info(f'Fetched {len(proxies)} proxies.')
    logging.info(f'Checked 0 proxies')
    for proxy in proxies:
        if checkproxy(proxy) == True: dorito.append(proxy); print("\r", end="", flush=True)