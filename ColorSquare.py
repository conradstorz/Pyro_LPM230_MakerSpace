# Nothing different here, just import the Pyro4 library along with whatever else you need

import os
import sys
import Pyro4

from ColorSquare_object import colorSquare

print( 'DISPLAY' in os.environ )
print( 'SSH_CONNECTION' in os.environ )
print( 'SSH_CLIENT' in os.environ )
print( 'SSH_TTY' in os.environ )

# Create a daemon -- Pyro's worker class to serve an object
daemon = Pyro4.Daemon()
# Get the URI of the daemon
uri = daemon.register(colorSquare)
# Find the nameserver on the network
try:
    ns = Pyro4.locateNS()
except:
    print('Nameserver not found.')
    sys.exit()
# Let the nameserver know what we answer to and where to find us
ns.register("square", uri)
# Listen for and handle requests
daemon.requestLoop()


