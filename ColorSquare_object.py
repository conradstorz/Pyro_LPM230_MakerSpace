

import Pyro4
import pygame
import time

# Tell Pyro to use a single instance of the class regardless of where the request originates
@Pyro4.behavior(instance_mode="single")
class colorSquare:
    # __init__ runs like normal, the only difference is it won't get called until something requests the Pyro object
    def __init__(self):
        # Standard PyGame init
        pygame.display.init()
        self.window = pygame.display.set_mode((256, 256))
        # Bookmark the start time
        self.start = time.time()

    # Pyro4.expose makes this function accessible to the outside world
    # Anything without expose is private
    # You can also expose the entire class if you want
    # Or declare @Pyro4.oneway which will make the call return None immediately and allow the remote process to run for as long as it needs to
    @Pyro4.expose
    def setColor(self, color):
        self.window.fill(color)
        pygame.display.flip()
        # Whatever you return will get passed back to the remote caller
        # All python types and simple classes are supported
        return "CUSTOM"

    @Pyro4.expose
    def setRed(self):
        self.window.fill((255, 0, 0))
        pygame.display.flip()
        return "RED"

    @Pyro4.expose
    def setGreen(self):
        self.window.fill((0, 255, 0))
        pygame.display.flip()
        return "GREEN"

    @Pyro4.expose
    def setBlue(self):
        self.window.fill((0, 0, 255))
        pygame.display.flip()
        return "BLUE"

    @Pyro4.expose
    def getTime(self):
        return time.time() - self.start


