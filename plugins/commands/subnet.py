import requests
from plugins.common import *

def subnet(domain):
    # validate domain
    if not checkserver(domain): logging.error('Please input a real domain'); return

    # get data from hackertarget
    r = requests.get(f'https://api.hackertarget.com/subnetcalc/?q={domain}')
    results = r.text.strip().split('\n')

    print(f"\n{gray}[{yellow}#{gray}] {white}Checking {yellow}{domain}{white} via {gray}hackertarget.com{white}...\n")
    print(f"{white}• {yellow}Hosts found:{white}")

    for result in results:
        print(f"  {gray}•{white} {result.replace('=', f':{yellow}')}")
    print('\n')
