import requests
import uuid
import hashlib
from plugins.common import *

def puuid(user):
    api = 'https://api.mojang.com/users/profiles/minecraft/'

    try:
        # fetch online uuid from mojang
        r = requests.get(f'{api}{user}')
        r_json = r.json()
        online_uuid = r_json['id']
        online_uuid = f'{online_uuid[0:8]}-{online_uuid[8:12]}-{online_uuid[12:16]}-{online_uuid[16:20]}-{online_uuid[20:32]}'

        # generate offline uuid
        offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{user}', 'utf-8')).digest()[:16], version=3))

        print(f"\n{gray}[{yellow}Premium{gray}] {white}{online_uuid}")
        print(f"{gray}[{yellow}Offline{gray}] {white}{offline_uuid}\n")

    except Exception:
        # fallback to offline if api fails
        offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{user}', 'utf-8')).digest()[:16], version=3))
        print(f"\n{gray}[{yellow}Offline{gray}] {white}{offline_uuid}\n")
