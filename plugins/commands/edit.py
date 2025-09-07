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

languages = ["english"]
themes = ["banana", "charcoal", "lily", "sunset", "snow"]

def edit(tf, value=None):
    global default

    # check if config exists
    if not os.path.exists("config.json"):
        logging.error("Config file does not exist.");
        return
    
    # load config
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)

    # compare keys against default
    keys = tf.split('.')
    ohio = default
    for k in keys:
        if not isinstance(ohio, dict) or k not in ohio: logging.error(f"Key invalid: {'.'.join(keys)}") ;return
        ohio = ohio[k]

    # nav to nested dict in config
    d = config
    for k in keys[:-1]:
        if not isinstance(d, dict) or k not in d:
            logging.error(f"Invalid Key: {'.'.join(keys)}")
            return

        d = d[k]
    
    final_key = keys[-1]

    # show values if no value is given
    if value is None:
        if tf == "language":
            logging.info(f"Values for language: {white}{','.join(languages)}")

        elif tf == "theme":
            logging.info(f"Values for theme: {white}{','.join(themes)}")

        return
    
    # convert value types
    if isinstance(d.get(final_key), bool) and isinstance(value, str):
        if value.lower() in ['true', '1', 'yes']:
            value = True

        elif value.lower() in ['false', '0', 'no']:
            value = False

    elif isinstance(d.get(final_key), int):
        try:
            value = int(value)
        except ValueError:
            logging.error("Value must be a number")
            return

    # update config and save
    d[final_key] = value
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    logging.success(f"{tf} = {value}")