import requests
from plugins.common import *

def target(domain):
    # validate domain
    if not checkserver(domain): logging.error('Please input a real domain'); return

    # get data from hackertarget
    r = requests.get(f'https://api.hackertarget.com/hostsearch/?q={domain}')
    results = r.text.strip().split('\n')
    
    # column width calculation
    iplen = max(len(x.split(',')[1]) for x in results) + 1
    domlen = max(len(x.split(',')[0]) for x in results) + 1

    print(f"\n{gray}[{yellow}#{gray}] {white}Checking {yellow}{domain}{white} via {gray}hackertarget.com{white}...\n")
    print(f"{white}• {yellow}Hosts found:{white}")

    for result in results:
        dom, ip = result.split(',')
        print(f"  {gray}•{white} {ip.ljust(iplen)}  {dom.ljust(domlen)}  {yellow}({is_protected(ip)})")
    print('\n')
