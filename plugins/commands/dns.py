import dns.resolver
from plugins.common import *

def lookup(domain):
    if not checkserver(domain):
        logging.error(f"{red}Please enter a valid domain{white}")
        return

    print(f"\n{gray}[{yellow}#{gray}] {white}Checking DNS records for {yellow}{domain}{white}...")

    records = ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT']
    for record in records:
        try:
            results = [r.to_text() for r in dns.resolver.resolve(domain, record)]
            print(f"{white}\n• {yellow}[{record}]:{white}")
            if results:
                for r in results:
                    print(f"{gray}•{white} {r}")
            else:
                print(f"{gray}•{red}No records found")
        except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            print(f"\n{white}• {yellow}[{record}]:{white}")
            print(f"{gray}• No records found")
        except dns.resolver.NXDOMAIN:
            logging.error(f"{red}Domain does not exist{white}")
            return
        except Exception as e:
            logging.error(f"{red}Error: {e}{white}")

    print()
