import dns.resolver
from plugins.common import *

def lookup(domain):
    if checkserver(domain):
        records = ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT']
        for record in records:
            try:
                results = [r.to_text() for r in dns.resolver.resolve(domain, record)]
                print(f"{yellow}[{white}{record}{yellow}]{white}")
                if results: [print(f"  - {r}") for r in results]
                else: print(f"{yellow}[{white}{record}{yellow}]{white} No records found")

            except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
                print(f"{yellow}[{white}{record}{yellow}]{white} No records found")

            except dns.resolver.NXDOMAIN:
                logging.error("Domain does not exist")
                return
            
            except Exception as e:
                logging.error(e)

    else: logging.error('Please enter a valid domain')
