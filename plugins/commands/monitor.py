from mcstatus import JavaServer
from plugins.common import *
import time

def monitor(s):
    if not checkserver(s): error('Please input a real domain or server'); return
    l=JavaServer.lookup(s);o=set()
    while True:
        try:
            n=set(l.query().players.names)
            for p in n-o: print(f'{p} joined the server')
            for p in o-n: print(f'{p} left the server')
            o=n
        except Exception as e: error(e)
        except KeyboardInterrupt: return