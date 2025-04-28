import os

def shell(port): # yes thats it and yes 45$ mcptool has this shit 💔💔
    os.system(f'ncat -lvnp {port}')