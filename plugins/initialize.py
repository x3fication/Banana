from plugins.common import *
from os import getlogin
import shutil
import requests
import subprocess

def pkgmngr():
    managers = {
        "apt": 1,
        "dnf": 2,
        "pacman": 3
    }

    for name, number in managers.items():
        if shutil.which(name):
            return number

    return None

def node():
    print('Downloading nodeJS')

    if os.name == 'nt':
        os.system('winget install OpenJS.NodeJS')
        time.sleep(2)
        logging.info('Installing mineflayer, express')
        subprocess.run(fr'"C:\Program Files/nodejs/npm.cmd" install mineflayer express socks', shell=True)

    elif os.name == 'posix':
        pm = pkgmngr()
        if pm == 1:
            os.system('sudo apt update')
            os.system('sudo apt install nodejs npm')

        if pm == 2:
            os.system('sudo dnf update')
            os.system('sudo dnf install nodejs npm')

        if pm == 3:
            os.system('sudo pacman -S nodejs npm')

        if pm in [1, 2, 3]:
            os.system('node -v')
            os.system('npm -v')
            os.system('npm install mineflayer express socks')

def velocity():
    logging.info('Downloading Velocity [PaperMC]')

    r = requests.get("https://api.papermc.io/v2/projects/velocity").json()
    version, build = r["versions"][-1], requests.get(f"https://api.papermc.io/v2/projects/velocity/versions/{r['versions'][-1]}").json()["builds"][-1]
    url = f"https://api.papermc.io/v2/projects/velocity/versions/{version}/builds/{build}/downloads/velocity-{version}-{build}.jar"
    fakeproxy_url = f"https://github.com/Renovsk/Plantain/releases/download/fp-1/plantain-fakeproxy-1.0.jar"
    jar = requests.get(url).content

    os.makedirs('./proxy/velocity/', exist_ok=True)
    with open('./proxy/velocity/velocity.jar', 'wb') as f:
        f.write(jar)

    logging.success(f'Done downloading velocity-{version}-{build}.jar')

    logging.info('Setting up FakeProxy')
    os.makedirs('./proxy/fakeproxy/plugins/', exist_ok=True)
    with open('./proxy/fakeproxy/velocity.jar', 'wb') as f: 
        f.write(jar)

    fp = requests.get(fakeproxy_url).content
    with open('./proxy/fakeproxy/plugins/plantain-fakeproxy-1.0.jar', 'wb') as f:
        f.write(fp)

    logging.success('Done downloading plantain-fakeproxy-1.0.jar')
    time.sleep(1)


def upd(): node(); velocity()

def initialize():
    if firstload() == True:
        print(fr"{yellow}{getstring('inithello')} {white}{getlogin()}{yellow},{getstring('initmsg')}")
        upd(); open("banana", "w").close()

    print("\033c", end="")
    animate()
    loadmenu()