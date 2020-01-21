import cherrypy
import Pyro4
from PWI_html import index_html


class web:
    def __init__(self):
        self.screens = list()
        #self.screens.append(Pyro4.Proxy("PYRONAME:scoreboard1"))
        self.screens.append(Pyro4.Proxy("PYRONAME:scoreboard2"))
        #self.screens.append(Pyro4.Proxy("PYRONAME:scoreboard3"))
        #self.screens.append(Pyro4.Proxy("PYRONAME:scoreboard4"))

        for screen in self.screens:
            screen.drawTitle()
            screen.update()

    @cherrypy.expose
    def index(self):
        return index_html

    @cherrypy.expose
    def updateTitle(self, screen, name):
        self.screens[int(screen) - 1].updateTitle(str(name))

    @cherrypy.expose
    def adjustScore(self, screen, delta):
        self.screens[int(screen) - 1].updateScore(int(delta))

    @cherrypy.expose
    def startTimers(self):
        for screen in self.screens:
            screen.startTimer()

        firstPlace = False
        while firstPlace == False:
            for screen in self.screens:
                if screen.timerRunning() == False:
                    screen.updateTitle("WINNER")
                    firstPlace = True


cherrypy.server.socket_host = "0.0.0.0"
cherrypy.quickstart(web(), "/")
