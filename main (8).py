import pygame, sys
from pygame.locals import QUIT
import time
import random

pygame.font.init()

WIDTH = 800
HEIGHT = 400

# notes for next time: beat game (make it easier)

doorLeftClosed = False
doorRightClosed = False

global power
global powerDrainRate

power = 99
powerTimer = 0
powerDrainRate = 1 / 36  # 9 - No use # 7 - One Use # 5 - Two Use, # 3 - All use
monitorUp = False
foxyDrain = 1

BLACK = (0, 0, 0)
DARKGREY = (50, 50, 50)
GREY = (100, 100, 100)
CRIMSON = (150, 0, 0)
DC = (50, 0, 0)
BROWN = (150, 75, 0)
PURPLE = (200, 0, 255)
RED = (255, 0, 0)
DARKRED = (85, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

background = pygame.Rect(0, 0, 800, 400)

doorLeft = pygame.Rect(100, 100, 150, 300)
doorRight = pygame.Rect(600, 100, 150, 300)
buttonLeft = pygame.Rect(300, 125, 50, 50)
buttonRight = pygame.Rect(500, 125, 50, 50)
monitor = pygame.Rect(30, 30, 740, 380)
cams = pygame.image.load('Cam_Map1.png')
bonnieDoor = pygame.image.load('BonnieDoor.png')
bonnieDoor = pygame.transform.scale(bonnieDoor, (150, 300))
chicaDoor = pygame.image.load('ChicaDoor.png')
chicaDoor = pygame.transform.scale(chicaDoor, (150, 300))
warning = pygame.image.load('Warning-signal.png')
warning = pygame.transform.scale(warning, (25, 25))
bonnieJump = pygame.image.load('BonnieJump.png')
bonnieJump = pygame.transform.scale(bonnieJump, (500, 400))
chicaJump = pygame.image.load('ChicaJump.png')
chicaJump = pygame.transform.scale(chicaJump, (500, 400))
foxyJump = pygame.image.load('FoxyJump.png')
foxyJump = pygame.transform.scale(foxyJump, (500, 400))
freddyJump = pygame.image.load('FreddyJump.png')
freddyJump = pygame.transform.scale(freddyJump, (500, 400))
freddyJump2 = pygame.image.load('FreddyJump2.png')
freddyJump2 = pygame.transform.scale(freddyJump2, (800, 400))

font = pygame.font.Font('freesansbold.ttf', 32)
powerLevel = font.render('Power: ' + str(round(power)) + "%", True, WHITE,
                         BLACK)
powerRect = powerLevel.get_rect()
powerRect.center = (80, 360)

clock = font.render("12 AM", True, WHITE, BLACK)
clockRect = powerLevel.get_rect()
clockRect.center = (750, 50)

sixam = font.render("6 AM", True, WHITE, BLACK)
sixamRect = powerLevel.get_rect()
sixamRect.center = (400, 200)

test = pygame.Rect(300, 300, 150, 150)

global chiCam
global foxCam
global fredCam

bonCam = "1A"
chiCam = "1A"
foxCam = "1C"
fredCam = "1A"

global bonC
global chiC
global foxC
global fredC

bonC = 0
chiC = 0
foxC = 0
fredC = 0

bonTime = 0
chiTime = 0
foxTime = 0
fredTime = 0
fredTime2 = 0

bonJump = False
chiJump = False
foxJump = False
fredJump = False
fredJump2 = False

nightTimer = 0


class Bonnie():

    def __init__(self):
        self.rect = pygame.Rect(340, 200, 25, 25)  #purple

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, PURPLE, self.rect)

    def update(self, x, y):
        self.rect = pygame.Rect(x, y, 25, 25)

    def move(self):
        global bonCam
        global bonJump
        if bonCam == "1A":
            bonCam = "1B"
        elif bonCam == "1B":
            bonC = random.randint(0, 1)
            if bonC == 0:
                bonCam = "2A"
            else:
                bonCam = "5"
        elif bonCam == "5":
            bonC = random.randint(0, 3)
            if bonC == 0:
                bonCam = "2A"
            else:
                bonCam = "1B"
        elif bonCam == "2A":
            bonC = random.randint(0, 3)
            if bonC == 3:
                bonCam = "3"
            elif bonC == 2:
                bonCam = "1B"
            else:
                bonCam = "2B"
        elif bonCam == "3":
            bonCam = "2A"
        elif bonCam == "2B":
            bonCam = "!"
        elif bonCam == "!":
            if doorLeftClosed:
                bonCam = "1B"
            else:
                bonJump = True


class Chica():

    def __init__(self):
        self.rect = pygame.Rect(400, 200, 25, 25)  #yellow

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, YELLOW, self.rect)

    def update(self, x, y):
        self.rect = pygame.Rect(x, y, 25, 25)

    def move(self):
        global chiCam
        global chiJump
        if chiCam == "1A":
            chiCam = "1B"
        elif chiCam == "1B":
            chiCam = "7"
        elif chiCam == "7":
            chiCam = "6"
        elif chiCam == "6":
            chiCam = "4A"
        elif chiCam == "4A":
            chiCam = "4B"
        elif chiCam == "4B":
            chiCam = "!"
        elif chiCam == "!":
            if doorRightClosed:
                chiCam = "1B"
            else:
                chiJump = True


class Foxy():

    def __init__(self):
        foxy = pygame.Rect(253, 194, 25, 25)  #red

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, RED, self.rect)

    def update(self, x, y):
        self.rect = pygame.Rect(x, y, 25, 25)

    def move(self):
        global foxCam
        global foxyDrain
        global power
        global foxJump
        if foxCam == "1C":
            foxCam = "1C2"
        elif foxCam == "1C2":
            foxCam = "1C3"
        elif foxCam == "1C3":
            foxCam = "2A"
        elif foxCam == "2A":
            if doorLeftClosed:
                power -= foxyDrain
                foxyDrain += 5
                foxCam = "1C"
            else:
                foxJump = True


class Freddy():

    def __init__self():
        freddy = pygame.Rect(-100, -100, 25, 25)  #brown

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, BROWN, self.rect)

    def update(self, x, y):
        self.rect = pygame.Rect(x, y, 25, 25)

    def move(self):
        global fredCam
        global fredJump
        if fredCam == "1A":
            fredCam = "1B"
        elif fredCam == "1B":
            fredCam = "7"
        elif fredCam == "7":
            fredCam = "6"
        elif fredCam == "6":
            fredCam = "4A"
        elif fredCam == "4A":
            fredCam = "4B"
        elif fredCam == "4B":
            if doorRightClosed:
                fredCam = "4A"
            else:
                fredCam = "!"
        elif fredCam == "!":
            fredJump = True


def drawBackground():
    pygame.draw.rect(DISPLAYSURF, CRIMSON, background)
    if doorLeftClosed:
        pygame.draw.rect(DISPLAYSURF, GREY, doorLeft)
        pygame.draw.rect(DISPLAYSURF, GREEN, buttonLeft)
    else:
        pygame.draw.rect(DISPLAYSURF, BLACK, doorLeft)
        pygame.draw.rect(DISPLAYSURF, RED, buttonLeft)
    if doorRightClosed:
        pygame.draw.rect(DISPLAYSURF, GREY, doorRight)
        pygame.draw.rect(DISPLAYSURF, GREEN, buttonRight)
    else:
        pygame.draw.rect(DISPLAYSURF, BLACK, doorRight)
        pygame.draw.rect(DISPLAYSURF, RED, buttonRight)


bonnie = Bonnie()
chica = Chica()
foxy = Foxy()
freddy = Freddy()

pygame.init()
DISPLAYSURF = pygame.display.set_mode((800, 400))
DISPLAYSURF.fill(CRIMSON)
pygame.display.set_caption('FNaF!')
while True:
    #print(pygame.mouse.get_pos())
    #print(power)
    if power >= 0:
        pygame.draw.rect(DISPLAYSURF, CRIMSON, background)
    else:
        pygame.draw.rect(DISPLAYSURF, DC, background)
    if doorLeftClosed and power >= 0:
        pygame.draw.rect(DISPLAYSURF, GREY, doorLeft)
        pygame.draw.rect(DISPLAYSURF, GREEN, buttonLeft)
    else:
        pygame.draw.rect(DISPLAYSURF, BLACK, doorLeft)
        if power >= 0:
            pygame.draw.rect(DISPLAYSURF, RED, buttonLeft)
        else:
            pygame.draw.rect(DISPLAYSURF, DARKRED, buttonLeft)
    if doorRightClosed and power >= 0:
        pygame.draw.rect(DISPLAYSURF, GREY, doorRight)
        pygame.draw.rect(DISPLAYSURF, GREEN, buttonRight)
    else:
        pygame.draw.rect(DISPLAYSURF, BLACK, doorRight)
        if power >= 0:
            pygame.draw.rect(DISPLAYSURF, RED, buttonRight)
        else:
            pygame.draw.rect(DISPLAYSURF, DARKRED, buttonRight)
    if monitorUp and power >= 0:
        pygame.draw.rect(DISPLAYSURF, DARKGREY, monitor)
        DISPLAYSURF.blit(cams, (200, 30))
        if bonCam == "1A":
            bonnie.update(370, 70)
        elif bonCam == "1B":
            bonnie.update(350, 140)
        elif bonCam == "5":
            bonnie.update(240, 90)
        elif bonCam == "2A":
            bonnie.update(345, 270)
        elif bonCam == "3":
            bonnie.update(280, 310)
        elif bonCam == "2B":
            bonnie.update(350, 380)
        elif bonCam == "!":
            bonnie.update(-100, -100)
        bonnie.draw()

        if chiCam == "1A":
            chica.update(440, 70)
        elif chiCam == "1B":
            chica.update(460, 140)
        elif chiCam == "7":
            chica.update(565, 170)
        elif chiCam == "6":
            chica.update(527, 286)
        elif chiCam == "4A":
            chica.update(459, 276)
        elif chiCam == "4B":
            chica.update(463, 380)
        elif chiCam == "!":
            chica.update(-100, -100)
        chica.draw()

        if foxCam == "1C":
            foxy.update(253, 194)
        elif foxCam == "1C2":
            foxy.update(267, 203)
        elif foxCam == "1C3":
            foxy.update(282, 205)
        elif foxCam == "2A":
            foxy.update(-100, -100)
            DISPLAYSURF.blit(warning, (366, 288))
        foxy.draw()

        if fredCam == "1A":
            freddy.update(405, 70)
        elif fredCam == "1B":
            freddy.update(405, 110)
        elif fredCam == "7":
            freddy.update(616, 162)
        elif fredCam == "6":
            freddy.update(568, 304)
        elif fredCam == "4A":
            freddy.update(462, 254)
        elif fredCam == "4B":
            freddy.update(450, 360)
        elif fredCam == "!":
            freddy.update(-100, -100)
        freddy.draw()
    else:
        if bonCam == "!":
            if doorLeftClosed == False:
                DISPLAYSURF.blit(bonnieDoor, (100, 100))

        if chiCam == "!":
            if doorRightClosed == False:
                DISPLAYSURF.blit(chicaDoor, (600, 100))
    if power >= 0:
        bonTime += 1
        chiTime += 1
        foxTime += 1
        fredTime += 1
    nightTimer += 1
    print(nightTimer)
    if bonCam != "!":
        if bonTime > random.randint(1800, 2300):
            bonnie.move()
            bonTime = 0
    else:
        if bonTime >= 1000:
            bonnie.move()
            bonTime = 0

    if chiCam != "!":
        if chiTime > random.randint(2800, 3300):
            chica.move()
            chiTime = 0
    else:
        if chiTime >= 1000:
            chica.move()
            chiTime = 0

    if foxCam != "2A":
        if monitorUp:
            foxTime = 0
        else:
            if foxTime > random.randint(2200, 2300):
                foxy.move()
                foxTime = 0
    else:
        if foxTime >= 750:
            foxy.move()
            foxTime = 0

    if fredCam != "!":
        if monitorUp:
            fredTime = 0
        else:
            if fredCam != "4A" and fredCam != "4B":
                if fredTime > random.randint(2600, 3600):
                    freddy.move()
                    fredTime = 0
            else:
                if fredTime > random.randint(1500, 1000):
                    freddy.move()
                    fredTime = 0
    else:
        if fredTime >= random.randint(1500, 2000):
            freddy.move()
            freddyTime = 0
    #print(bonTime)
    #print(chiTime)
    #print(foxTime)
    #print(fredTime)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if buttonRight.collidepoint(pos):
                if doorRightClosed == False:
                    doorRightClosed = True
                    pygame.draw.rect(DISPLAYSURF, GREEN, buttonRight)
                    pygame.draw.rect(DISPLAYSURF, GREY, doorRight)
                else:
                    doorRightClosed = False
                    pygame.draw.rect(DISPLAYSURF, RED, buttonRight)
                    pygame.draw.rect(DISPLAYSURF, BLACK, doorRight)

            if buttonLeft.collidepoint(pos):
                if doorLeftClosed == False:
                    doorLeftClosed = True
                    pygame.draw.rect(DISPLAYSURF, GREEN, buttonLeft)
                    pygame.draw.rect(DISPLAYSURF, GREY, doorLeft)
                else:
                    doorLeftClosed = False
                    pygame.draw.rect(DISPLAYSURF, RED, buttonLeft)
                    pygame.draw.rect(DISPLAYSURF, BLACK, doorLeft)
        if not bonJump and not chiJump and not foxJump and not fredJump:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if monitorUp == False:
                        power -= 0.25
                        monitorUp = True
                        pygame.draw.rect(DISPLAYSURF, DARKGREY, monitor)
                    else:
                        monitorUp = False
        else:
            monitorUp = False

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if monitorUp:
        if doorLeftClosed:
            if doorRightClosed:
                powerDrainRate = 10 / 28
            else:
                powerDrainRate = 10 / 20
        else:
            if doorRightClosed:
                powerDrainRate = 10 / 20
            else:
                powerDrainRate = 10 / 28
    else:
        if doorLeftClosed:
            if doorRightClosed:
                powerDrainRate = 1 / 20
            else:
                powerDrainRate = 1 / 28
        else:
            if doorRightClosed:
                powerDrainRate = 1 / 28
            else:
                powerDrainRate = 1 / 36

    powerTimer += 1
    if powerTimer >= 125:
        power -= powerDrainRate
        powerTimer = 0
    if power < 0:
        power = -0.3
        fredTime2 += 1
        if fredTime2 >= 5000:
            fredJump2 = True

    if bonJump:
        drawBackground()
        DISPLAYSURF.blit(bonnieJump, (150, 0))
        monitorUp = False
        bonCam = "1A"
        pygame.display.update()
        time.sleep(999999999)
        quit()
    if chiJump:
        drawBackground()
        DISPLAYSURF.blit(chicaJump, (150, 0))
        monitorUp = False
        chiCam = "1A"
        pygame.display.update()
        time.sleep(999999999)
        quit()
    if foxJump:
        drawBackground()
        DISPLAYSURF.blit(foxyJump, (150, 0))
        monitorUp = False
        foxCam = "1C"
        pygame.display.update()
        time.sleep(999999999)
        quit()
    if fredJump:
        drawBackground()
        DISPLAYSURF.blit(freddyJump, (150, 0))
        monitorUp = False
        fredCam = "1A"
        pygame.display.update()
        time.sleep(999999999)
    if fredJump2:
        DISPLAYSURF.blit(freddyJump2, (0, 0))
        monitorUp = False
        pygame.display.update()
        time.sleep(999999999)
    DISPLAYSURF.blit(powerLevel, powerRect)
    powerLevel = font.render('Power: ' + str(round(power)) + "%", True, WHITE,
                             BLACK)
    DISPLAYSURF.blit(clock, clockRect)
    if nightTimer < 25000:
        # 12AM
        clock = font.render("12 AM", True, WHITE, BLACK)
    if nightTimer >= 25000 and nightTimer < 50000:
        # 1AM
        clock = font.render("1 AM", True, WHITE, BLACK)
    if nightTimer >= 50000 and nightTimer < 75000:
        # 2AM
        clock = font.render("2 AM", True, WHITE, BLACK)
    if nightTimer >= 75000 and nightTimer < 100000:
        # 3AM
        clock = font.render("3 AM", True, WHITE, BLACK)
    if nightTimer >= 100000 and nightTimer < 125000:
        # 4AM
        clock = font.render("4 AM", True, WHITE, BLACK)
    if nightTimer >= 125000 and nightTimer < 150000:
        # 5AM
        clock = font.render("5 AM", True, WHITE, BLACK)
    if nightTimer >= 150000:
        pygame.draw.rect(DISPLAYSURF, BLACK, background)
        DISPLAYSURF.blit(sixam, sixamRect)
        pygame.display.update()
        time.sleep(999999999)
        quit()
    pygame.display.update()
