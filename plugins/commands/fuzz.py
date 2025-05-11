import requests
from plugins.common import *
from fake_useragent import UserAgent
import threading

def fuzzit(url):
    try:
        ua = UserAgent()
        r = requests.get(f"http://{url}", timeout=5, headers={"User-Agent": ua.random})
        if r.status_code == 200:
            logging.success(f"{yellow}[{white}FOUND{yellow}]{white} {url} (200 OK)")
    except requests.RequestException:
        pass

def fuzz(domain, file, mthreads):
    try:
         if checkserver(domain) == False: logging.error('Please input a real domain'); return
         mthreads = int(mthreads)
         domain = str(domain).replace('https://', '').replace('http://', '')
         with open(file, 'r') as f:
             fuzzing = [line.strip() for line in f if line.strip()]

         threads = []
         for sbsd in fuzzing:
             url = domain.replace('FUZZ', sbsd)
             while threading.active_count() > mthreads:
                 pass
             t = threading.Thread(target=fuzzit, args=(url,), daemon=True)
             t.start()
             threads.append(t)

         for t in threads:
             t.join()

    except Exception as e: logging.error(e)