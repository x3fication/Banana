import requests
from plugins.common import *

def ipinfo(ip):
    try:
        
        if checkip(ip) == False: error('Please enter a valid IP address.'); return
        r = requests.get(f'https://ipinfo.io/{ip}/json').json()
        for key, value in r.items():
            if key != "readme":
                print(f"{yellow}[{white}{key}{yellow}]{white} {value}")

        else: error("No data found for the given IP.")
    except Exception as e: error(f"Error: {e}")