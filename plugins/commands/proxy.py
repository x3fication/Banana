import subprocess, os, random
from plugins.common import *
import string

def proxy(ip, mode):
    try:
        p = "proxy/velocity"
        secret = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(43))
        with open(f"{p}/forwarding.secret", "w", encoding="utf-8") as f:
            f.write(secret)
        if not checkserver(ip): error('Please input a real domain or server'); return
        port = random.randint(20000, 30000)
        if not os.path.exists(p): os.makedirs(p)

        config = f"""
# Config version. Do not change this
config-version = "2.7"

bind = "0.0.0.0:{port}"

motd = "<#09add3>A Velocity Server"

show-max-players = 500

online-mode = true

force-key-authentication = true

prevent-client-proxy-connections = false

player-info-forwarding-mode = "{mode}"

forwarding-secret-file = "forwarding.secret"

announce-forge = false

kick-existing-players = false

ping-passthrough = "DISABLED"

sample-players-in-ping = false

enable-player-address-logging = true

[servers]
default = "{ip}"
try = [ "default" ]

[forced-hosts]
"example.com" = [ "default" ]

[advanced]
compression-threshold = 256
compression-level = -1
login-ratelimit = 3000
connection-timeout = 5000
read-timeout = 30000
haproxy-protocol = false
tcp-fast-open = false
bungee-plugin-message-channel = true
show-ping-requests = false
failover-on-unexpected-server-disconnect = true
announce-proxy-commands = true
log-command-executions = false
log-player-connections = true
accepts-transfers = false
enable-reuse-port = false
command-rate-limit = 50
forward-commands-if-rate-limited = true
kick-after-rate-limited-commands = 0
tab-complete-rate-limit = 10
kick-after-rate-limited-tab-completes = 0

[query]
enabled = false
port = {port}
map = "Velocity"
show-plugins = false
"""

        with open(f"{p}/velocity.toml", "w") as f:
            f.write(config)

        if not os.path.isfile(f"{p}/velocity.jar"):
            error(f"Could not find velocity.jar in {p}")
            return

        subprocess.run(["java", "-jar", "velocity.jar"], cwd=p)
        info(f'Proxy started on 0.0.0.0:{port}')

    except KeyboardInterrupt: pass