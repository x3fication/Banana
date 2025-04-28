import subprocess, os, random, requests, string, toml
from plugins.common import *

def proxy(ip, mode):
    try:
        p = "proxy/velocity"
        if mode not in ['modern', 'legacy', 'none', 'bungeeguard']: error('The valid modes are -> none, legacy, bungeeguard, modern'); return
        secret = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(43))
        if not os.path.exists(p): os.makedirs(p)
        with open(f"{p}/forwarding.secret", "w", encoding="utf-8") as f:
            f.write(secret)
        if not checkserver(ip): error('Please input a real domain or server'); return
        port = random.randint(20000, 30000)
        config_url = "https://raw.githubusercontent.com/PaperMC/Velocity/refs/heads/dev/3.0.0/proxy/src/main/resources/default-velocity.toml"
        response = requests.get(config_url)
        if response.status_code != 200: error("Failed to download config"); return
        config = toml.loads('\n'.join(line for line in response.text.splitlines() if not line.strip().startswith("#") and line.strip()))
        config['bind'] = f"0.0.0.0:{port}"
        config['player-info-forwarding-mode'] = mode
        config['forwarding-secret-file'] = "forwarding.secret"
        config['ping-passthrough'] = "DISABLED"
        config['announce-forge'] = False
        config['servers'] = { 'lobby': f"{ip}" }
        config['try'] = ["lobby"]
        config['forced-hosts'] = { "example.com": ["lobby"] }
        config['advanced']['compression-threshold'] = 256
        config['advanced']['compression-level'] = -1
        config['advanced']['login-ratelimit'] = 3000
        config['advanced']['connection-timeout'] = 5000
        config['advanced']['read-timeout'] = 30000
        config['advanced']['bungee-plugin-message-channel'] = True
        config['query']['enabled'] = False
        config['query']['port'] = port
        config['query']['map'] = "Velocity"
        config['query']['show-plugins'] = False
        with open(f"{p}/velocity.toml", "w", encoding="utf-8") as f:
            toml.dump(config, f)
        if not os.path.exists(f"{p}/plugins"): os.makedirs(f"{p}/plugins")
        os.system("java -jar velocity.jar")
    except Exception as e:
        error(f"Proxy error: {e}")
