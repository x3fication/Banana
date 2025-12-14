from plugins.common import *
from plugins.commands.dns import lookup
from plugins.commands.target import target
from plugins.commands.subnet import subnet

# yes that's it fuck you

def analyze(host):
    lookup(host)
    subnet(host)
    target(host)