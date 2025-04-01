# Pygame template - skeleton for a new pygame project
import pygame
import random

# WIDTH = 1280
# HEIGHT = 720
WIDTH = 500
HEIGHT = 500
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255 ,0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("War Simulation")
clock = pygame.time.Clock()

class Clan():
    def __init__(self, colorRGB, coords):
        self.colorRGB = colorRGB
        self.numFighters = 0
        self.captain = Captain(coords)
        self.fighters = []
    
    def spawnInitFighters(self, count):
        for i in range(0, count):
            self.spawnRandomFighter()


    def spawnRandomFighter(self):
        primaryClass = random.choice(["t", "d", "a"])
        coords = [self.captain.rect.x + random.randrange(-50,50), self.captain.rect.y + random.randrange(-50,50)]
        newFighter = Fighter(primaryClass, coords)
        self.fighters.append(newFighter)
        self.numFighters += 1
    
    def spawnPrimaryFighter(self):
        pass

class Captain():
    def __init__(self, coords):
        self.rect = pygame.Rect(coords[0], coords[1], 20, 20)

class Fighter():
    def __init__(self, initClass, coords):
        self.fighterClass = initClass
        self.rect = pygame.Rect(0,0,0,0)
        match initClass:
            case "t":
                self.health = 300
                self.attack = 25
                self.rect = pygame.Rect(coords[0], coords[1], 10, 10)
            case "d":
                self.health = 100
                self.attack = 150
                self.rect = pygame.Rect(coords[0], coords[1], 5, 10)
            case "a":
                self.health = 50
                self.attack = 100
                self.rect = pygame.Rect(coords[0], coords[1], 5, 5)

wallMargin = 100 - 20
redClan = Clan(RED, (wallMargin, wallMargin))
blueClan = Clan(BLUE, (WIDTH - wallMargin, HEIGHT - wallMargin))
yellowClan = Clan(YELLOW, (wallMargin, HEIGHT - wallMargin))
greenClan = Clan(GREEN, (WIDTH - wallMargin, wallMargin))
clans = [redClan, blueClan, yellowClan, greenClan]

for clan in clans:
    clan.spawnInitFighters(10)

# Game loop
running = True
while running:

    ## CALUCLATIONS

    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Colliding

    ## DRAWING TO SCREEN

    win.fill(WHITE)

    for clan in clans:
        
        win.fill(BLACK, pygame.Rect(clan.captain.rect.x - 2, clan.captain.rect.y - 2, clan.captain.rect.width + 4, clan.captain.rect.height + 4))
        win.fill(clan.colorRGB, clan.captain.rect)

        for fighter in clan.fighters:
            win.fill(BLACK, pygame.Rect(fighter.rect.x - 1, fighter.rect.y - 1, fighter.rect.width + 2, fighter.rect.height +2))
            win.fill(clan.colorRGB, fighter.rect)
            

    pygame.display.flip()

pygame.quit()