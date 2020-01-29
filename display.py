import sys

try:
    import RPi.GPIO as GPIO
    GPIO.setmode ( GPIO.BCM )
except ImportError as e:    
    print('This code runs directly on a Raspberry Pi only.')
    sys.exit(1)

import Pyro4
import pygame
import time
from Get_IP_address2 import get_ip
THIS_SERVER_IP = get_ip()
SCOREBOARDNAME = 'scoreboard2'
print(f'My name is:{SCOREBOARDNAME} and my IP is:{THIS_SERVER_IP}')



@Pyro4.behavior(instance_mode="single")
class scoreboard:
    def __init__ ( self ):
        print ("Starting Scoreboard")
        pygame.display.init()
        self.screen = pygame.display.set_mode ( ( 1280 ,720 ) , pygame.FULLSCREEN )
        print ("Setting full screen 1280x720")

        pygame.font.init()
        self.scoreFont = pygame.font.Font ( "00TT.TTF" , 300 )
        self.titleFont = pygame.font.Font ( "00TT.TTF" , 400 )
        print ("Fonts initialized")

        self.background = pygame.image.load ( "pu1280x720.png" ).convert()
        self.screen.blit ( self.background , ( 0 , 0 ) )
        print ("Background loaded")

        self.scoreGoal = 0
        self.currentScore = 0

        self.teamName = "ARTS"
        self.titleColor = ( 250 , 218 , 94 )

        self.oldRect = None

        self.startTime = None
        self.endTime = None
        self.running = False

        GPIO.setup ( 14 , GPIO.IN , pull_up_down=GPIO.PUD_UP )
        GPIO.add_event_detect ( 14 , GPIO.FALLING , callback=self.bumpPoints )

        print ("Done with init")

    def bumpPoints ( self , channel ):
        self.updateScore ( 10 )

    @Pyro4.oneway
    def updateTitle ( self , name ):
        self.teamName = name
        self.screen.blit ( self.background , ( 0 , 0 ) )

        self.drawTitle()
        self.drawScoreLocal()
        pygame.display.flip()

    @Pyro4.expose
    def timerRunning ( self ):
        return self.running

    @Pyro4.oneway
    def drawTitle ( self ):
        title = self.titleFont.render ( self.teamName , True , self.titleColor )
        X = self.screen.get_width() / 2 - title.get_width() / 2
        self.screen.blit ( title , ( X , 10 ) )
        print ("Draw Title")

    @Pyro4.oneway
    def drawScore ( self ):
        self.drawScoreLocal()
        print ("Draw Score")

    def drawScoreLocal ( self ):
        score = self.scoreFont.render ( str ( self.currentScore ) , True , ( 255 , 255 , 255 ) )
        shadow = self.scoreFont.render ( str ( self.currentScore ) , True , ( 0 , 0 , 0 ) )

        X = self.screen.get_width() / 2 - score.get_width() / 2

        blitArea = pygame.rect.Rect ( 0 , 400 , 1280 , 300 )
        self.screen.blit ( self.background , blitArea , blitArea )

        self.screen.blit ( shadow , ( X + 5 , 405 ) )
        self.screen.blit ( score , ( X , 400 ) )
        pygame.display.update ( [ blitArea ] )
        print ("Draw score local")

    @Pyro4.oneway
    def updateScore ( self , scoreDelta ):
        self.scoreGoal += scoreDelta
        nextUpdate = time.time() + .01

        while self.scoreGoal != self.currentScore:
            if time.time() < nextUpdate: continue
            nextUpdate = time.time() + .01

            print (self.scoreGoal , self.currentScore)

            if self.scoreGoal < self.currentScore:
                self.currentScore -= 5
                self.drawScoreLocal()
            elif self.scoreGoal > self.currentScore:
                self.currentScore += 5
                self.drawScoreLocal()
        print ("Update score")

    @Pyro4.oneway
    def startTimer ( self ):
        self.startTime = time.time()
        self.running = True
        self.updateTimer()

    def updateTimer ( self ):
        nextUpdate = time.time() + .01
        while self.running == True:
            if time.time() < nextUpdate: continue
            nextUpdate = time.time() + .01

            elapsed = time.time() - self.startTime
            score = self.scoreFont.render ( "{0:03.3f}".format ( elapsed ) , True , ( 255 , 255 , 255 ) )
            shadow = self.scoreFont.render ( "{0:03.3f}".format ( elapsed ) , True , ( 0 , 0 , 0 ) )

            X = self.screen.get_width() / 2 - score.get_width() / 2

            blitArea = pygame.rect.Rect ( 0 , 400 , 1280 , 300 )
            self.screen.blit ( self.background , blitArea , blitArea )

            self.screen.blit ( shadow , ( X + 5 , 405 ) )
            self.screen.blit ( score , ( X , 400 ) )
            pygame.display.update ( [ blitArea ] )

            if GPIO.input ( 14 ) == 0: self.running = False
        print ("update Timer")


    @Pyro4.oneway
    def update ( self ):
        pygame.display.flip()
        print ("update")


Pyro4.config.HOST = THIS_SERVER_IP
Pyro4.Daemon.serveSimple ( {
    scoreboard: SCOREBOARDNAME
    } , ns=True
    )

""" from pygame.org docs:
 pygame.display.set_mode()
    Initialize a window or screen for display
    set_mode(size=(0, 0), flags=0, depth=0, display=0) -> Surface
    This function will create a display Surface. The arguments passed in are requests for a display type. The actual created display will be the best possible match supported by the system.
    The size argument is a pair of numbers representing the width and height. The flags argument is a collection of additional options. The depth argument represents the number of bits to use for color.
    The Surface that gets returned can be drawn to like a regular Surface but changes will eventually be seen on the monitor.
    If no size is passed or is set to (0, 0) and pygame uses SDL version 1.2.10 or above, the created Surface will have the same size as the current screen resolution. If only the width or height are set to 0, the Surface will have the same width or height as the screen resolution. Using a SDL version prior to 1.2.10 will raise an exception.
    It is usually best to not pass the depth argument. It will default to the best and fastest color depth for the system. If your game requires a specific color format you can control the depth with this argument. Pygame will emulate an unavailable color depth which can be slow.
    When requesting fullscreen display modes, sometimes an exact match for the requested size cannot be made. In these situations pygame will select the closest compatible match. The returned surface will still always match the requested size.
    On high resolution displays(4k, 1080p) and tiny graphics games (640x480) show up very small so that they are unplayable. SCALED scales up the window for you. The game thinks it's a 640x480 window, but really it can be bigger. Mouse events are scaled for you, so your game doesn't need to do it.
    The flags argument controls which type of display you want. There are several to choose from, and you can even combine multiple types using the bitwise or operator, (the pipe "|" character). If you pass 0 or no flags argument it will default to a software driven window. Here are the display flags you will want to choose from:

    pygame.FULLSCREEN    create a fullscreen display
    pygame.DOUBLEBUF     recommended for HWSURFACE or OPENGL
    pygame.HWSURFACE     hardware accelerated, only in FULLSCREEN
    pygame.OPENGL        create an OpenGL-renderable display
    pygame.RESIZABLE     display window should be sizeable
    pygame.NOFRAME       display window will have no border or controls
    pygame.SCALED        resolution depends on desktop size and scale graphics

    New in pygame 2.0.0: SCALED

    For example:
    # Open a window on the screen
    screen_width=700
    screen_height=400
    screen=pygame.display.set_mode([screen_width,screen_height])

    The display index 0 means the default display is used.
    The display argument is new with pygame 1.9.5.
"""