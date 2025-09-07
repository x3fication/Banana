import subprocess, os, random
from plugins.common import *
import string

def fakeproxy(ip, mode):
    try:
        if mode not in ['modern', 'none', 'bungeeguard', 'legacy']:
            logging.info('Modes: none, legacy, bungeeguard, modern')
            return

        p = "proxy/fakeproxy"

        # create dir and save forwarding secret
        secret = ''.join(random.choices(string.ascii_letters + string.digits, k=43))
        with open(f"{p}/forwarding.secret", "w", encoding="utf-8") as f:
            f.write(secret)
        
        # validate server
        if not checkserver(ip):
            logging.error('Please input a real domain or server')
            return
        
        # get port
        cfg = bananac()
        port = cfg["server"]["port"]
        if cfg["server"]["randomize_port"]:
            port = random.randint(20000, 30000)

        # load config template
        template = "./plugins/files/config.txt"
        if not os.path.isfile(template):
            logging.error(f"Config not find template: {template}")
            return

        with open(template, "r") as f:
            config = f.read()

        # replace placeholders
        config = config.replace("PORT_HERE", str(port))
        config = config.replace("IP_HERE", ip)
        config = config.replace("FORWARDING_MODE", mode)

        # write final config
        with open(f"{p}/velocity.toml", "w", encoding="UTF-8") as f:
            f.write(config)

        # check for velocity.jar
        if not os.path.isfile(f"{p}/velocity.jar"):
            logging.error(f"Could not find velocity.jar in {p}")
            return
        
        logging.info(f'Proxy started on 0.0.0.0:{port}')
        subprocess.run(["java", "-jar", "velocity.jar"], cwd=p)

    except KeyboardInterrupt: pass