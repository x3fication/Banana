from plugins.common import *
import json
import os

default = {
    "language": "english",
    "theme": "banana",
    "server": {
        "port": 23457,
        "randomize_port": False
    }
}

def edit(tf, value):
    global default
    if not os.path.exists("config.json"): logging.error("Config file does not exist."); return
    with open("config.json", 'r', encoding='utf-8') as f: config = json.load(f)
    keys = tf.split('.')
    for k in keys:
        if not isinstance(default, dict) or k not in default:
            logging.error(f"Key invalid: {'.'.join(keys)}")
            return
        default = default[k]
    d = config
    for k in keys[:-1]:
        if k not in d:
            logging.error(f"Invalid Key: {'.'.join(keys)}")
            return
        d = d[k]
    final_key = keys[-1]
    if isinstance(d.get(final_key), bool) and isinstance(value, str):
        if value.lower() in ['true', '1', 'yes']: value = True
        elif value.lower() in ['false', '0', 'no']: value = False
    elif isinstance(d.get(final_key), int):
        try: value = int(value)
        except ValueError:
            logging.error("Value must be a number")
            return
    d[final_key] = value
    with open('config.json', 'w', encoding='utf-8') as f: json.dump(config, f, indent=2)
    logging.success(f"{tf} = {value}")