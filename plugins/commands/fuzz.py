import requests
from plugins.common import *
from fake_useragent import UserAgent

def fuzz(domain, file):
    ua = UserAgent()
    domain = str(domain).replace('https://', '').replace('http://', '')
    with open(file, 'r') as f:
        fuzzing = [line.strip() for line in f if line.strip()]
        
    for sbsd in fuzzing:
        url = domain.replace('FUZZ', sbsd)
        try:
            r = requests.get(f"http://{url}", timeout=5, headers={"User-Agent": ua.random})
            if r.status_code == 200:
                success(f"{yellow}[{white}FOUND{yellow}]{white} {url} (200 OK)")
        except requests.RequestException:
            pass