from plugins.common import *
import requests
from bs4 import BeautifulSoup

def iphistory(domain):
    # clean up domain input
    gg = domain.replace('https://', '').replace('http://', '').replace('www.', '')

    # validate domain
    if not checkserver(gg):
        logging.error('Please input a real domain')
        return

    print(f"\n{gray}[{yellow}#{gray}] {white}Checking {yellow}{domain}{white} via {gray}viewdns.info{white}...\n")

    # fetch history
    try:
        r = requests.get(
            f'https://viewdns.info/iphistory/?domain={gg}',
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=10
        )
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    # parse html using beautifulsoup
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find_all('tr')

    # extract ip history table data
    data = [
        [c.text.strip() for c in row.find_all('td')[:4]]
        for row in rows
        if len(row.find_all('td')) >= 4
    ]

    if not data:
        print("No records found")
        return

    # table headers and column width calculation
    heads = ["IP Address", "Location", "Owner", "Last Seen"]
    widths = [max(len(head), *(len(row[i]) for row in data)) for i, head in enumerate(heads)]

    # create table separators
    sep_top = f"{gray}┌{'─'*(widths[0]+2)}┬{'─'*(widths[1]+2)}┬{'─'*(widths[2]+2)}┬{'─'*(widths[3]+2)}┐"
    sep_mid = f"{gray}├{'─'*(widths[0]+2)}┼{'─'*(widths[1]+2)}┼{'─'*(widths[2]+2)}┼{'─'*(widths[3]+2)}┤"
    sep_bottom = f"└{'─'*(widths[0]+2)}┴{'─'*(widths[1]+2)}┴{'─'*(widths[2]+2)}┴{'─'*(widths[3]+2)}┘"

    # print table header
    print(sep_top)
    print(f"{gray}│ {yellow}{heads[0].ljust(widths[0])} {gray}│ {yellow}{heads[1].ljust(widths[1])} {gray}│ {yellow}{heads[2].ljust(widths[2])} {gray}│ {yellow}{heads[3].ljust(widths[3])} {gray}│")
    print(sep_mid)

    # print table rows in reverse (latest first)
    for row in reversed(data):
        print(f"{gray}│ {yellow}{row[0].ljust(widths[0])} {gray}│ {white}{row[1].ljust(widths[1])} {gray}│ {white}{row[2].ljust(widths[2])} {gray}│ {white}{row[3].ljust(widths[3])} {gray}│")

    print(sep_bottom + "\n")
