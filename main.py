import pygame
import random
import math

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
        self.speed = 100  # Speed for normalization, can be adjusted for faster/slower movement
        self.numFighters = 0
        self.captain = Captain(coords)
        self.fighters = []
        self.lastMove = [0,0]

    
    def spawnInitFighters(self, count):
        for i in range(0, count):
            self.spawnRandomFighter()


    def spawnRandomFighter(self):
        primaryClass = random.choice(["t", "d", "a"])
        coords = [self.captain.x + random.randrange(-50,50), self.captain.y + random.randrange(-50,50)]
        newFighter = Fighter(primaryClass, coords)
        self.fighters.append(newFighter)
        self.numFighters += 1
    
    def findClosestCaptain(self, clans):
        if clans[0] == self:
            closestClan = clans[1]
        else:
            closestClan = clans[0]
        for clan in clans:
            if clan != self:
                currentClanDistance = math.sqrt(math.pow(clan.captain.x - self.captain.x, 2) + math.pow(clan.captain.y - self.captain.y, 2))
                closestClanDistance = math.sqrt(math.pow(closestClan.captain.x - self.captain.x, 2) + math.pow(closestClan.captain.y - self.captain.y, 2))
                if currentClanDistance < closestClanDistance:
                    closestClan = clan
        return closestClan

    def moveCaptain(self, clans, delta_time):
        closestClan = self.findClosestCaptain(clans)
        if (math.sqrt(math.pow(closestClan.captain.x - self.captain.x, 2) + math.pow(closestClan.captain.y - self.captain.y, 2))) > 100:

            distance = [closestClan.captain.x - self.captain.x, closestClan.captain.y - self.captain.y]
            normalisedDistance = normalise(distance)

            # Update captain's position with fractional movement
            self.captain.x += normalisedDistance[0] * self.speed * delta_time
            self.captain.y += normalisedDistance[1] * self.speed * delta_time
            self.lastMove = normalisedDistance

class Captain():
    def __init__(self, coords):
        self.x = float(coords[0])  # Store position as float for smooth movement
        self.y = float(coords[1])  # Store position as float for smooth movement
        self.rect = pygame.Rect(int(self.x), int(self.y), 20, 20)

    def update_rect(self):
        # Update the rect to match the (x, y) position, rounding to nearest integer
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

class Fighter():
    def __init__(self, initClass, coords):
        self.fighterClass = initClass
        self.x = coords[0]
        self.y = coords[1]
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
    
    def updateRect(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

def normalise(nums):
    x = nums[0]
    y = nums[1]

    # Find the maximum absolute value
    max_val = max(abs(x), abs(y))
    
    # Normalize the coordinates
    if max_val != 0:
        normalized_x = x / max_val
        normalized_y = y / max_val
    else:
        normalized_x = 0
        normalized_y = 0
    
    return [normalized_x, normalized_y]

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
clansMoveFrame = 0
while running:

    # Get the delta_time for consistent movement
    delta_time = clock.get_time() / 1000.0  # Time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clansMoveFrame += 1 
    if clansMoveFrame >= 5:
        for clan in clans:
            clan.moveCaptain(clans, delta_time)
        clansMoveFrame = 0

    ## DRAWING TO SCREEN

    win.fill(WHITE)

    for clan in clans:
        # Update the captain rect based on floating point position
        clan.captain.update_rect()

        win.fill(BLACK, pygame.Rect(clan.captain.rect.x - 2, clan.captain.rect.y - 2, clan.captain.rect.width + 4, clan.captain.rect.height + 4))
        win.fill(clan.colorRGB, clan.captain.rect)

        for fighter in clan.fighters:
            win.fill(BLACK, pygame.Rect(fighter.rect.x - 1, fighter.rect.y - 1, fighter.rect.width + 2, fighter.rect.height + 2))
            win.fill(clan.colorRGB, fighter.rect)

    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()
