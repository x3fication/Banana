from plugins.common import *
import requests
from bs4 import BeautifulSoup

def iphistory(domain):
    gg = domain.replace('https://', '').replace('http://', '').replace('www.', '')
    if checkserver(gg) == False: logging.error('Please input a real domain'); return
    print(f"\n{gray}[{yellow}#{gray}] {white}Checking {yellow}{domain}{white} via {gray}viewdns.info{white}...\n")
    r = requests.get(f'https://viewdns.info/iphistory/?domain={gg}', headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        return

    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:
            data.append([c.text.strip() for c in cols[:4]])

    if not data:
        print("No records")
        return

    heads = ["IP Address", "Location", "Owner", "Last Seen"]
    widths = [len(h) for h in heads]
    for row in data:
        for i in range(4):
            widths[i] = max(widths[i], len(row[i]))

    print(f"{gray}┌{'─'*(widths[0]+2)}┬{'─'*(widths[1]+2)}┬{'─'*(widths[2]+2)}┬{'─'*(widths[3]+2)}┐")
    print(f"{gray}│ {yellow}{heads[0].ljust(widths[0])} {gray}│ {yellow}{heads[1].ljust(widths[1])} {gray}│ {yellow}{heads[2].ljust(widths[2])} {gray}│ {yellow}{heads[3].ljust(widths[3])} {gray}│")
    print(f"{gray}├{'─'*(widths[0]+2)}┼{'─'*(widths[1]+2)}┼{'─'*(widths[2]+2)}┼{'─'*(widths[3]+2)}┤")

    for row in reversed(data):
        print(f"{gray}│ {yellow}{row[0].ljust(widths[0])} {gray}│ {white}{row[1].ljust(widths[1])} {gray}│ {white}{row[2].ljust(widths[2])} {gray}│ {white}{row[3].ljust(widths[3])} {gray}│")

    print(f"└{'─'*(widths[0]+2)}┴{'─'*(widths[1]+2)}┴{'─'*(widths[2]+2)}┴{'─'*(widths[3]+2)}┘\n")

