from plugins.common import *
from os import getlogin
import shutil
import requests
import subprocess

def pkgmngr():
    if shutil.which('apt'):
        return 1
    elif shutil.which('dnf'):
        return 2
    elif shutil.which('pacman'):
        return 3
    else: return None

def node():
    print('Downloading nodeJS')

    if os.name == 'nt':
        os.system(r'winget install OpenJS.NodeJS')
        time.sleep(2)
        os.system('npm install mineflayer express')


    elif os.name == 'posix':
        pm = pkgmngr()
        if pm == 1:
            os.system('sudo apt update')
            os.system('sudo apt install nodejs npm')
            os.system('node -v')
            os.system('npm -v')
            os.system('npm install mineflayer express')

        if pm == 2:
            os.system('sudo dnf update')
            os.system('sudo dnf install nodejs npm')
            os.system('node -v')
            os.system('npm -v')
            os.system('npm install mineflayer express')

        if pm == 3:
            os.system('sudo pacman -S nodejs npm')
            os.system('node -v')
            os.system('npm -v')
            os.system('npm install mineflayer express')

def velocity():
    info('Downloading Velocity [PaperMC]')
    download = requests.get(f"https://mineacademy.org/api/velocity/latest")
    os.makedirs('./proxy/velocity/', exist_ok=True)
    with open('./proxy/velocity/velocity.jar', 'wb') as f:
        f.write(download.content)
    success(f'Done downloading Velocity')
    time.sleep(1)

def waterfall():
    info('Downloading Waterfall [PaperMC]')
    download = requests.get(f"https://mineacademy.org/api/waterfall/latest")
    os.makedirs('./proxy/waterfall/', exist_ok=True)
    with open('./proxy/waterfall/waterfall.jar', 'wb') as f:
        f.write(download.content)
    success(f'Done downloading Waterfall')
    time.sleep(1)

def upd(): # this is prob retarded way to do it ik
    node()
    velocity()
    waterfall()

def initialize():
    if firstload() == True:
        print(fr'''{yellow}
 _
//\
V  \
 \  \_         
  \,'.`-.                                        
   |\ `. `.                                      Hello {white}{getlogin()}{yellow},
   ( \  `. `-.                        _,.-:\     please wait while we setup your environment.
    \ \   `.  `-._             __..--' ,-';/
     \ `.   `-.   `-..___..---'   _.--' ,'/
      `. `.    `-._        __..--'    ,' /
        `. `-_     ``--..''       _.-' ,'
          `-_ `-.___        __,--'   ,'
             `-.__  `----"""    __.-'
                  `--..____..--'
        ''')
        node()
        velocity()
        waterfall()
        animate()
        loadmenu()

    elif firstload() == False: animate(); loadmenu()
    