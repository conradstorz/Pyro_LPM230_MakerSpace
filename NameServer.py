import Pyro4

# Find the nameserver
ns = Pyro4.locateNS()
# Ask the nameserver for the URI to the remote object we want
uri = ns.lookup("square")
# Create a connection to the remote object
remoteSquare = Pyro4.Proxy(uri)

# Repeat as necessary for multiple remote objects

while 1:
    request = input("What color? ")
    # Treat the remote object above as if it is local
    # The return value (just printed here) is whatever the remote function wants to send back (if anything)
    if request == "RED":
        print(remoteSquare.setRed())
    elif request == "GREEN":
        print(remoteSquare.setGreen())
    elif request == "BLUE":
        print(remoteSquare.setBlue())
    elif request == "TIME":
        print(
            "The square has been running for "
            + str(remoteSquare.getTime())
            + " seconds"
        )
    else:
        # fail gracefully if we can't decode 3 numbers separated by commas
        try:
            RGB = request.split(",")
            print(remoteSquare.setColor((int(RGB[0]), int(RGB[1]), int(RGB[2]))))
        except:
            print("Couldn't parse an R,G,B argument")
