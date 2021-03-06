#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" RaspberryPi 'RPi' code to put a fullscreen display on a remotely
controlled screen.
"""

#TODO detect if running directly on the console of RPi, exit with warning otherwise.
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import Pyro4
import pygame
import time

# TODO move this module active code from bottom of file to here,
# after testing that it is working where it is now.
# This file has not yet been tested 1/17/2020


@Pyro4.behavior(instance_mode="single")
class scoreboard:
    def __init__(self):
        print("Starting Scoreboard")
        pygame.display.init()
        self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        print("Setting full screen 1280x720")

        pygame.font.init()
        self.scoreFont = pygame.font.Font("00TT.TTF", 300)
        self.titleFont = pygame.font.Font("00TT.TTF", 400)
        print("Fonts initialized")

        self.background = pygame.image.load("pu1280x720.png").convert()
        self.screen.blit(self.background, (0, 0))
        print("Background loaded")

        self.scoreGoal = 0
        self.currentScore = 0

        self.teamName = "ARTS"
        self.titleColor = (250, 218, 94)

        self.oldRect = None

        self.startTime = None
        self.endTime = None
        self.running = False

        GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(14, GPIO.FALLING, callback=self.bumpPoints)

        print("Done with init")

    def bumpPoints(self, channel):
        self.updateScore(10)

    @Pyro4.oneway
    def updateTitle(self, name):
        self.teamName = name
        self.screen.blit(self.background, (0, 0))

        self.drawTitle()
        self.drawScoreLocal()
        pygame.display.flip()

    @Pyro4.expose
    def timerRunning(self):
        return self.running

    @Pyro4.oneway
    def drawTitle(self):
        title = self.titleFont.render(self.teamName, True, self.titleColor)
        X = self.screen.get_width() / 2 - title.get_width() / 2
        self.screen.blit(title, (X, 10))
        print("Draw Title")

    @Pyro4.oneway
    def drawScore(self):
        self.drawScoreLocal()
        print("Draw Score")

    def drawScoreLocal(self):
        score = self.scoreFont.render(
            str(self.currentScore), True, (255, 255, 255)
        )
        shadow = self.scoreFont.render(
            str(self.currentScore), True, (0, 0, 0)
        )

        X = self.screen.get_width() / 2 - score.get_width() / 2

        blitArea = pygame.rect.Rect(0, 400, 1280, 300)
        self.screen.blit(self.background, blitArea, blitArea)

        self.screen.blit(shadow, (X + 5, 405))
        self.screen.blit(score, (X, 400))
        pygame.display.update([blitArea])
        print("Draw score local")

    @Pyro4.oneway
    def updateScore(self, scoreDelta):
        self.scoreGoal += scoreDelta
        nextUpdate = time.time() + 0.01

        while self.scoreGoal != self.currentScore:
            if time.time() < nextUpdate:
                continue
            nextUpdate = time.time() + 0.01

            print(self.scoreGoal, self.currentScore)

            if self.scoreGoal < self.currentScore:
                self.currentScore -= 5
                self.drawScoreLocal()
            elif self.scoreGoal > self.currentScore:
                self.currentScore += 5
                self.drawScoreLocal()
        print("Update score")

    @Pyro4.oneway
    def startTimer(self):
        self.startTime = time.time()
        self.running = True
        self.updateTimer()

    def updateTimer(self):
        nextUpdate = time.time() + 0.01
        while self.running:
            if time.time() < nextUpdate:
                continue
            nextUpdate = time.time() + 0.01

            elapsed = time.time() - self.startTime
            score = self.scoreFont.render(
                "{0:03.3f}".format(elapsed), True, (255, 255, 255)
            )
            shadow = self.scoreFont.render(
                "{0:03.3f}".format(elapsed), True, (0, 0, 0)
            )

            X = self.screen.get_width() / 2 - score.get_width() / 2

            blitArea = pygame.rect.Rect(0, 400, 1280, 300)
            self.screen.blit(self.background, blitArea, blitArea)

            self.screen.blit(shadow, (X + 5, 405))
            self.screen.blit(score, (X, 400))
            pygame.display.update([blitArea])

            if GPIO.input(14) == 0:
                self.running = False
        print("update Timer")

    @Pyro4.oneway
    def update(self):
        pygame.display.flip()
        print("update")


# TODO move this to top of file

Pyro4.config.HOST = "10.10.10.114"

NameServerFound = False
while not NameServerFound:
    try:
        Pyro4.Daemon.serveSimple(
            {scoreboard: "scoreboard2"}, 
            ns=True
        )
        NameServerFound = True
    except Pyro4.errors.NamingError:  # appears server is not running
        print("Nameserver not yet found.")
        NameServerFound = False
        time.sleep(5)

