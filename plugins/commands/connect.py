from plugins.common import *
import requests

def connect(username, server, proxy=None):
    try:
        connected = False

        # validate server
        if not checkserver(server):
            logging.error("Please input a real domain or server")
            return
        

        if ':' in server:
            server, port = str(server).split(':')
        else:
            port = 25565

        # make payload
        payload = {"host": server, "port": port, "username": username}
        if proxy is not None:
            payload["proxy"] = ranproxy()

        # attempt connection
        response = requests.post('http://localhost:6969/connect', json=payload)

        if response.status_code not in [200, 400]:
            logging.error(f'Failed to connect [{response.status_code}]')
            return

        # wait for connection
        for _ in range(10):
            r = requests.get('http://localhost:6969/status').json()[server + ':' + str(port)][username]['connected']
            if r: connected = True; break
            logging.info('Waiting for connection...')
            time.sleep(2)

        if not connected:
            logging.error("Failed to connect within timeout.")
            return

        logging.info('Type "exit" to exit. [beta] This is still very basic but works for sending messages')

        # main message loop
        while True:
            msg = input("> ").strip()
            if msg.lower() == "exit":
                # disconnect bot
                status = requests.get("http://localhost:6969/status").json()
                if status.get(f"{server}:{port}", {}).get(username, {}).get("connected"):
                    requests.post("http://localhost:6969/disconnect", json={"host": server, "port": port, "username": username})
                    logging.info("Bot disconnected.")
                else:
                    logging.info("Bot already disconnected.")
                return

            # send message
            r = requests.post(
                "http://localhost:6969/send",
                json={"host": server, "port": port, "username": username, "message": msg}
            )
            if r.status_code != 200:
                logging.error(f"Failed to send message. (BOT is disconnected) [{r.status_code}]")
                return

    except KeyboardInterrupt:
        requests.post('http://localhost:6969/disconnect', json={"host": server, "port": port, "username": username})
        return

    except Exception as e: 
        logging.error(e)