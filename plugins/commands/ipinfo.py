import requests
import socket
from plugins.common import *

import requests
import socket
from plugins.common import *

def ipinfo(server):
    try:
        # resolve domain to ip
        try:
            ip = socket.gethostbyname(server)
        except socket.gaierror:
            ip = server 

        # validate ip
        if not checkip(ip):
            logging.error('Please enter a valid IP address or domain.')
            return

        # fetch ip info
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,isp,org,proxy,mobile,hosting")
        data = response.json()

        # check if request was good
        if data.get("status") != "success":
            logging.error(f"API error: {data.get('message')}")
            return

        print(f"\n{gray}[{yellow}#{gray}] {white}Checking {yellow}{ip}{white} via {gray}ip-api.com{white}...\n")
        print(f"{white}• {yellow}IP Information:{white}")
        print(f"  {gray}•{white} {'Country:'.ljust(15)}{green}{data['country']}")
        print(f"  {gray}•{white} {'ISP:'.ljust(15)}{white}{data['isp']}")
        print(f"  {gray}•{white} {'Organization:'.ljust(15)}{white}{data['org']}")
        print(f"  {gray}•{white} {'Proxy/VPN:'.ljust(15)}{green if not data['proxy'] else red}{data['proxy']}")
        print(f"  {gray}•{white} {'Hosting/DC:'.ljust(15)}{green}{data['hosting']}")
        print(f"  {gray}•{white} {'Mobile Conn:'.ljust(15)}{green}{data['mobile']}\n")

    except Exception as e:
        logging.error(f"Error: {e}")
