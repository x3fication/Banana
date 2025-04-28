def parse(text): # yes this is retarded but if it works don't touch it 😂😂😂
    text = text.replace('§0', '\033[30m').replace('§1', '\033[34m').replace('§2', '\033[32m').replace('§3', '\033[36m')\
               .replace('§4', '\033[31m').replace('§5', '\033[35m').replace('§6', '\033[33m').replace('§7', '\033[37m')\
               .replace('§8', '\033[90m').replace('§9', '\033[94m').replace('§a', '\033[92m').replace('§b', '\033[96m')\
               .replace('§c', '\033[91m').replace('§d', '\033[95m').replace('§e', '\033[93m').replace('§f', '\033[97m')\
               .replace('§l', '\033[1m').replace('§o', '\033[3m').replace('§n', '\033[4m').replace('§m', '\033[9m')\
               + '\033[0m'
    return text
