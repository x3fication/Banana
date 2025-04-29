<h1 align="center">
  <img src="https://r2.e-z.host/049cab41-5ed3-4a5c-a42f-5b83b721f333/re5pq23l.png" alt="Header Image" style="width:30%; max-width:600px;"/>
</h1>


# Banana
This is a free & better alternative to MCPTool

# Installation
## Requirements 
- Python 3.10+
- winget package manager (Windows)

## Get a local copy up and running
```
Open Terminal and run: 
git clone https://github.com/Renovsk/Banana.git && cd Banana
pip3 install -r requirements.txt
python3 main.py

Install the command line developer tools if prompted
```

# Features
## Commands

| Command   | Arguments         | Description                                                         |
|-----------|-------------------|---------------------------------------------------------------------|
| `server`  | `<address>`        | Shows information about the server                                  |
| `uuid`    | `<ign>`            | Shows player's UUID                                                 |
| `ipinfo`  | `<ip>`             | Shows information about the given IP                                |
| `monitor` | `<ip>`             | Monitors who leaves and joins on a specified server (if queries are enabled) |
| `dns`     | `<domain>`         | Shows all DNS records of the domain                                 |
| `proxy`   | `<ip> <mode>`      | Starts a local Velocity proxy server that redirects to the specified server |
| `check`   | `<file>`           | Check the status of Minecraft servers listed in a specified text file |
| `scan`    | `<ip> <range> <threads>` | Check the status of Minecraft servers listed in a specified text file. Example: `scan 0.0.0.0 1-65535 10` |
| `clear`   | N/A               | Clears the screen                                                    |
| `update`  | N/A               | Re-initializes Banana                                                |
| `kick`    | `<username> <server>` | Kicks a player from the server (if cracked)                          |
| `shell`   | `<port>`           | Uses netcat to listen to a port                                      |
| `connect` | `<username> <server>` | Joins with a bot and allows you to send messages                     |
| `rcon`    | `<server> <password>` | Connects to a server's RCON                                         |
| `brutrcon`| `<server> <file>`  | Tries the passwords of the file given to try to connect to RCON     |
| `fuzz`    | `<website> <file> <threads>` | Example: `example.com/FUZZ` or `FUZZ.example.com`                   |
| `sendcmd` | `<username> <server> <file>` | Sends a bot that will execute a list of commands from a file        |


MORE SOON!

## Credits
- Made by @x5ten on discord
