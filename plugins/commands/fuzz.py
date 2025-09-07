import requests
from plugins.common import *
from fake_useragent import UserAgent
import threading

def fuzzit(url, sem):
    try:
        ua = UserAgent()
        r = requests.get(f"http://{url}", timeout=5, headers={"User-Agent": ua.random})
        if r.status_code == 200:
            logging.success(f"{yellow}[{white}FOUND{yellow}]{white} {url} (200 OK)")
    except requests.RequestException:
        pass
    finally:
        sem.release()  # release the semaphore when thread finishes

def fuzz(domain, file, max_threads):
    try:
        if not checkserver(domain):
            logging.error("Please input a real domain")
            return

        domain = domain.replace("https://", "").replace("http://", "")
        max_threads = int(max_threads)

        sem = threading.Semaphore(max_threads)

        with open(file, "r", encoding="utf-8") as f:
            fuzzing = [line.strip() for line in f if line.strip()]

        threads = []

        for entry in fuzzing:
            url = domain.replace("FUZZ", entry)
            sem.acquire()  # wait until there's room for a new thread
            t = threading.Thread(target=fuzzit, args=(url, sem), daemon=True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    except Exception as e:
        logging.error(e)
