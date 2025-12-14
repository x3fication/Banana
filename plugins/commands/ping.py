from plugins.common import *
import socket
import time


def ping(host, port):

    print(f"\n{gray}[{yellow}#{gray}] {white}Connecting to {yellow}{host}{white} on {yellow}TCP {port}\n")
    failed = 0
    connected = 0
    try:
        while True:
            start = time.time()
            try:
                # makes connection with the host
                s = socket.create_connection((host, port), timeout=3)
                s.close()
                ms = (time.time() - start) * 1000

                logging.success(f"{white}Connected to {yellow}{host}{white}: time={yellow}{ms:.2f}ms {white}protocol={yellow}TCP{white} port={yellow}{port}")
                connected += 1

            # if failed connection add 1 to failed var
            except socket.timeout:
                logging.error("Connection timed out")
                failed += 1

            except ConnectionRefusedError:
                logging.error("Connection refused")
                failed +=1

            except Exception as e:
                logging.error(f"{e}")
            time.sleep(1)
    
    # on ctrl+c print total attempts of thingy and yea
    except KeyboardInterrupt:
            logging.info(f"{white}Connected = {yellow}{connected}{white}, Failed = {yellow}{failed}{white}, Total = {yellow}{failed + connected}")
            