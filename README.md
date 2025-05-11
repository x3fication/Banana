
<h1 align="center">
  <img src="https://r2.e-z.host/049cab41-5ed3-4a5c-a42f-5b83b721f333/re5pq23l.png" alt="Header Image" style="width:30%; max-width:600px;"/>
</h1>

# Banana 🍌

**A free and better alternative to MCPTool**

---

## 📦 Installation

### Requirements

* Python 3.10+
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

| Command     | Arguments                                              | Description                                                                  |
| ----------- | ------------------------------------------------------ | ---------------------------------------------------------------------------- |
| `dns`       | `<domain>`                                             | Shows all DNS records of the domain                                          |
| `uuid`      | `<ign>`                                                | Shows player's UUID                                                          |
| `scan`      | `<ip> <range> <threads>`                               | Scans for online Minecraft servers in a given IP range                       |
| `kick`      | `<username> <server>`                                  | Kicks a player from the server (if cracked)                                  |
| `rcon`      | `<server> <password>`                                  | Connects to a server's RCON                                                  |
| `fuzz`      | `<website> <file> <threads>`                           | URL fuzzing: e.g., `example.com/FUZZ` or `FUZZ.example.com`                  |
| `exit`      | N/A                                                    | Exits this fuckass app                                                       |
| `proxy`     | `<ip> <mode>`                                          | Starts a local Velocity proxy server that redirects to the specified server  |
| `check`     | `<file>`                                               | Checks the status of Minecraft servers listed in a specified text file       |
| `clear`     | N/A                                                    | Clears the screen                                                            |
| `ogmur`     | `<users_file> <server> <commands_file> <stay_logged>`  | Sends a bot that will execute a list of commands from a file                 |
| `shell`     | `<host> <port> <bind_port>`                            | Uses netcat to listen to a port                                              |
| `server`    | `<address>`                                            | Shows information about the server                                           |
| `ipinfo`    | `<ip>`                                                 | Shows information about the given IP                                         |
| `target`    | `<domain>`                                             | Shows all subdomains with their resolved IPs                                 |
| `update`    | N/A                                                    | Re-initializes Banana                                                        |
| `monitor`   | `<ip>`                                                 | Monitors who leaves and joins on a specified server (if queries are enabled) |
| `connect`   | `<username> <server>`                                  | Joins with a bot and allows you to send messages                             |
| `sendcmd`   | `<username> <server> <commands_file>`                  | Sends a bot that executes commands from a file                               |
| `brutrcon`  | `<server> <file>`                                      | Attempts to brute-force RCON using a password file                           |
| `fakeproxy` | `<ip> <mode>`                                          | Starts a Velocity proxy server that logs all commands sent to the server     |
| `example`   | `<name>`                                               | Example command for demonstration purposes                                   |

> More commands coming soon!

---

## 👉 Credits

* Made by `@x5ten` on Discord
