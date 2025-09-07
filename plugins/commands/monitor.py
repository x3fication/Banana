from mcstatus import JavaServer
from plugins.common import *
import time

def monitor(s):
    # validate server
    if not checkserver(s):
        logging.error('Please input a real domain or server')
        return

    # lookup server
    server = JavaServer.lookup(s)
    old = set()

    while True:
        try:
            # get current online players
            new = set(server.query().players.names)

            # detect joins
            for player in new - old:
                print(f'{player} joined the server')

            # detect leaves
            for player in old - new:
                print(f'{player} left the server')

            # update previous players
            old = new

        except KeyboardInterrupt:
            return
        except Exception as e:
            logging.error(e)
