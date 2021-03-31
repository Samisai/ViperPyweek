# Default libraries

import pygame
from sys import exit
from time import process_time as pt  # seconds

# Custom libraries

import shapesHelpers


# TODO make stuff look nicer, add blocks behind selection, make buttons change color when hovered, shooting star background

# library initializations
pygame.init()
window = pygame.display.set_mode((400, 400))  # creating pygame window
shapesHelpers.init(window)
pygame.display.set_caption("Space Force")

# The below assets will need to be changed to your own paths

# constants
MARSIMG = pygame.image.load(r"src\assets\mars.png")
SPLASHIMG = pygame.image.load(
    r"src\assets\splashScreen.png").convert()
FONT = pygame.font.Font(r"src\assets\gameFont.ttf", 35)
WHITE = (255, 255, 255)

# button location constants

ORIGIN = (0, 0)

EXITBUTTONXSTART, EXITBUTTONXEND = 170, 305
EXITBUTTONYSTART, EXITBUTTONYEND = 250, 135

STARTBUTTONXSTART, STARTBUTTONXEND = 160, 140
STARTBUTTONYSTART, STARTBUTTONYEND = 150, 135

RESUMEBUTTONXSTART, RESUMEBUTTONXEND = 150, 260
RESUMEBUTTONYSTART, RESUMEBUTTONYEND = 150, 185

MENUBUTTONXSTART, MENUBUTTONXEND = 130, 260
MENUBUTTONYSTART, MENUBUTTONYEND = 250, 285

# Vars

accelRate = 1
iterCt = 0
menuDisp = True
pauseDisp = False
splashed = False
mars = MARSIMG

# Classes (before vars as some vars may depend on classes)


class Acceleration():
    def __init__(self, currentSpeed, maxSpeed, rate):
        self.startSpeed = currentSpeed
        self.currentSpeed = currentSpeed
        self.maxSpeed = maxSpeed
        self.rate = rate
        self.startTime = pt()
        self.loopAcc = True

    def __str__(self):
        try:
            self.averageAcceleration = self.avgAccel()
            return f"""
Reached terminal velocity:
{self.time} seconds passed in accelerating to
{self.maxSpeed} from {self.startSpeed} with a rate of {self.rate} units.
The average acceleration was {self.averageAcceleration} units/s
                    """
        except Exception as e:
            return

    def accelerate(self):
        if self.currentSpeed < self.maxSpeed:
            self.currentSpeed += self.rate
            pygame.time.wait(100)
        elif self.currentSpeed == self.maxSpeed and self.loopAcc:
            self.time = pt() - self.startTime
            self.loopAcc = False
        return self.currentSpeed

    def avgAccel(self):
        return (self.currentSpeed - self.startSpeed)/self.time


acceleration = Acceleration(0, 10, accelRate)


# methods for visualizing

# planet functions


def drawPlanet(planetSprite):
    """
    This function draws the planet sprite that was loaded 
    in the position that will be used for the game, this
    is needed as there will be multiple levels with different
    planet sprites
    """
    window.blit(planetSprite, (0, 275))


def rotatePlanet(planet):  # https://www.pygame.org/wiki/RotateCenter?parent=CookBook
    """
    This function takes in the planet sprite and velocity that
    is desired for rotation, negative velocity will move the
    opposite direction, set the initial planet equal to the
    return of this function
    """
    origPlanet = planet.get_rect()
    accel = acceleration.accelerate()
    rotatedPlanet = pygame.transform.rotate(planet, accel)
    planetRect = origPlanet.copy()
    planetRect.center = rotatedPlanet.get_rect().center
    finalRotate = rotatedPlanet.subsurface(planetRect).copy()
    return finalRotate

# button and prompting functions


def mainMenu():
    """Generates the main menu and buttons"""
    exitButton = FONT.render('Exit', True, WHITE)
    window.blit(exitButton, (EXITBUTTONXSTART, EXITBUTTONYSTART))
    startButton = FONT.render('Start', True, WHITE)
    window.blit(startButton, (STARTBUTTONXSTART, STARTBUTTONYSTART))


def pauseScreen():
    """Generates the pause screen and buttons"""
    shapesHelpers.rect(0, 0, 400, 400, red=0, green=0,
                       blue=0)  # commenting this out can make the pause screen transparent
    resumeButton = FONT.render('Resume', True, WHITE)
    window.blit(resumeButton, (RESUMEBUTTONXSTART, RESUMEBUTTONYSTART))
    menuButton = FONT.render('Main Menu', True, WHITE)
    window.blit(menuButton, (MENUBUTTONXSTART, MENUBUTTONYSTART))


def inputMgmt():
    """Manages all input and events"""
    global pauseDisp, menuDisp, splashed
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if 260 >= mouse[0] >= 150 and 250 <= mouse[1] <= 285 and menuDisp and splashed:
                pygame.quit()
                exit()
            elif 260 >= mouse[0] >= 150 and 150 <= mouse[1] <= 185 and menuDisp and splashed:
                menuDisp = False
            elif 260 >= mouse[0] >= 150 and 150 <= mouse[1] <= 185 and pauseDisp:
                pauseDisp = False
            elif 260 >= mouse[0] >= 150 and 250 <= mouse[1] <= 285 and pauseDisp:
                pauseDisp = False
                menuDisp = True
        if keys[pygame.K_ESCAPE] and not menuDisp and pauseDisp:
            pauseDisp = False
        elif not menuDisp and keys[pygame.K_ESCAPE]:
            pauseScreen()
            pauseDisp = True
        elif not splashed and keys[pygame.K_SPACE]:
            splashed = True
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()


# Other


def splashScrDisp():
    """Generates splash screen at launch"""
    pressSpace = FONT.render('Press Space', True, WHITE)
    window.blit(SPLASHIMG, ORIGIN)
    window.blit(pressSpace, (105, 300))


def printAcceleration():
    global iterCt
    if iterCt < 1:
        try:
            print(acceleration)
            iterCt += 1
        except TypeError:
            pass

 # Mainloop


while True:
    pygame.time.wait(100)
    inputMgmt()
    if not splashed:
        splashScrDisp()
    if splashed:
        if not pauseDisp:
            shapesHelpers.rect(1, 1, 400, 400, red=0, green=0, blue=0)
        if not menuDisp and not pauseDisp:
            drawPlanet(mars)
            mars = rotatePlanet(mars)
        if menuDisp:
            mainMenu()
    printAcceleration()
    pygame.display.update()  # updates the display
