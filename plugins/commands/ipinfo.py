import requests
from plugins.common import *

def ipinfo(ip):
    ohio = checkip(ip)
    if ohio == True:
        r = requests.get(f'https://ipinfo.io/{ip}/json').json()
        host = r['hostname']
        city = r['city']
        region = r['region']
        country = r['country']
        print(f"""{yellow}[{white}Host{yellow}]{white} {host}
{yellow}[{white}City{yellow}]{white} {city}
{yellow}[{white}Region{yellow}]{white} {region}
{yellow}[{white}Country{yellow}]{white} {country}""")
        
    else: error('Please enter a Valid IP Address')