
<h1 align="center">
  <img src="https://files.catbox.moe/nqvuai.png" alt="Header Image" style="width:30%; max-width:600px;"/>
</h1>

# Banana 🍌

**A free and better alternative to MCPTool**

---

## 📦 Installation

### Requirements

* Python 3.10+ (don't forget to add to path)
* Winget package manager (Windows only)

### Setup

```bash
git clone https://github.com/Renovsk/Banana.git && cd Banana
pip install -r requirements.txt
python main.py
```

---

## ⚙️ Features

### Commands

| Command       | Arguments                                                     | Description                                                     |
| ------------- | ------------------------------------------------------------- | --------------------------------------------------------------- |
| `websearch`   | N/A                                                           | Opens the web search utility                                    |
| `server`      | `<address>`                                                   | Shows information about the server                              |
| `edit`        | `<key> <value>`                                               | Edits the banana config                                         |
| `bungeeguard` | `<ip> <bungeeguard_token>`                                    | Makes a BungeeGuard proxy                                       |
| `uuid`        | `<ign>`                                                       | Shows player's UUID                                             |
| `ipinfo`      | `<ip>`                                                        | Shows information about the given IP                            |
| `fetch`       | `<type>`                                                      | Scrapes proxies of a given type                                 |
| `monitor`     | `<ip>`                                                        | Monitors who leaves and joins a server (requires query support) |
| `dns`         | `<domain>`                                                    | Shows all DNS records of the domain                             |
| `target`      | `<domain>`                                                    | Shows all subdomains with their resolved IPs                    |
| `proxy`       | `<ip> <mode>`                                                 | Starts a Velocity proxy redirecting to the server               |
| `fakeproxy`   | `<ip> <mode>`                                                 | Starts a Velocity proxy that logs all commands                  |
| `check`       | `<file>`                                                      | Checks the status of servers listed in a file                   |
| `mcscan`      | `<ip> <range> <threads>`                                      | Scans a range of ports on a given IP for Minecraft servers      |
| `scan`        | `<ip> <range> <threads>`                                      | Performs multi-threaded TCP port scan on a given IP             |
| `clear`       | N/A                                                           | Clears the screen                                               |
| `ogmur`       | `<users_file> <server> <commands_file> <stay_logged> <proxy>` | Sends a bot to execute commands from a file                     |
| `update`      | N/A                                                           | Re-initializes Banana                                           |
| `kick`        | `<username> <server> <proxy>`                                 | Kicks a player from the server (if cracked)                     |
| `shell`       | `<host> <port> <bind_port>`                                   | Uses netcat to listen on a port                                 |
| `connect`     | `<username> <server> <proxy>`                                 | Joins with a bot and allows messaging                           |
| `rcon`        | `<server> <password>`                                         | Connects to a server’s RCON                                     |
| `brutrcon`    | `<server> <file>`                                             | Tries passwords from file to brute-force RCON                   |
| `fuzz`        | `<website> <file> <threads>`                                  | URL fuzzing (e.g., `example.com/FUZZ` or `FUZZ.example.com`)    |
| `sendcmd`     | `<username> <server> <commands_file> <proxy>`                 | Sends a bot that executes commands from a file                  |
| `exit`        | N/A                                                           | Exits the app                                                   |

> More commands coming soon!

---

## 👉 Credits
* Made by `@x5ten` on Discord

You are not allowed to sell banana or any modified versions. If you use any of my code please give me credit.

![Alt](https://repobeats.axiom.co/api/embed/7e4e4960a018472a371a835b4c2924118d6e3c1c.svg "Repobeats analytics image")
