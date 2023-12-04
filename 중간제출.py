import pygame
import random
from pygame.rect import *


pygame.init()
pygame.display.set_caption("final DDR")

def resultProcess(direction):
    global isColl, score, DrawResult, result_ticks

    if isColl and CollDirection.direction == direction:
        score += 10
        CollDirection.y = -1
        DrawResult = 1
    else:
        DrawResult = 2
    result_ticks = pygame.time.get_ticks()

def eventProcess():
    global isActive, score, chance
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isActive = False
            if chance > 0:
                if event.key == pygame.K_UP:  # 0
                    resultProcess(0)
                if event.key == pygame.K_LEFT:  # 1
                    resultProcess(1)
                if event.key == pygame.K_DOWN:  # 2
                    resultProcess(2)
                if event.key == pygame.K_RIGHT:  # 3
                    resultProcess(3)
            else:
                if event.key == pygame.K_SPACE:
                    score = 0
                    chance = chance_MAX
                    for direc in Directions:
                        direc.y = -1

class Direction(object):
    def __init__(self):
        self.pos = None
        self.direction = 0
        self.image = pygame.image.load(f"리듬게임/direction.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rotated_image = pygame.transform.rotate(self.image, 0)
        self.y = -1
        self.x = int(SCREEN_WIDTH*0.75)-(self.image.get_width()/2)

    def rotate(self, direction=0):
        self.direction = direction
        self.rotated_image = pygame.transform.rotate(
            self.image, 90*self.direction)

    def draw(self):
        if self.y >= SCREEN_HEIGHT:
            self.y = -1
            return True
        elif self.y == -1:
            return False
        else:
            self.y += 1
            self.pos = screen.blit(self.rotated_image, (self.x, self.y))
            return False

def drawIcon():
    global start_ticks,chance

    if chance <= 0:
        return

    elapsed_time = (pygame.time.get_ticks() - start_ticks)
    if elapsed_time > 400:
        start_ticks = pygame.time.get_ticks()
        for direc in Directions:
            if direc.y == -1:
                direc.y = 0
                direc.rotate(direction=random.randint(0, 3))
                break

    for direc in Directions:
        if direc.draw():            
            chance -= 1


def setText():
    global score, chance
    mFont = pygame.font.SysFont("굴림", 40)

    mtext = mFont.render(f'score : {score}', True, 'black')
    screen.blit(mtext, (10, 10, 0, 0))

    mtext = mFont.render(f'chance : {chance}', True, 'black')
    screen.blit(mtext, (10, 42, 0, 0))

    if chance <= 0:
        mFont = pygame.font.SysFont("굴림", 90)
        mtext = mFont.render(f'Game over!!', True, 'red')
        tRec = mtext.get_rect()
        tRec.centerx = SCREEN_WIDTH/2
        tRec.centery = SCREEN_HEIGHT/2 - 40
        screen.blit(mtext, tRec)

def drawResult():
    global DrawResult, result_ticks
    if result_ticks > 0:
        elapsed_time = (pygame.time.get_ticks() - result_ticks)
        if elapsed_time > 400:
            result_ticks = 0
            DrawResult = 0
    screen.blit(resultImg[DrawResult], resultImgRec)

isActive = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
chance_MAX = 30
score = 0
chance = chance_MAX
isColl = False
CollDirection = 0
DrawResult, result_ticks = 0,0
start_ticks = pygame.time.get_ticks()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Directions = [Direction() for i in range(0, 10)]
targetArea = Rect(SCREEN_WIDTH/2, 400, SCREEN_WIDTH/2, 80)
resultFileNames = ["리듬게임/normal.png", "리듬게임/good.png", "리듬게임/bad.png"]
resultImg = []
for i, name in enumerate(resultFileNames):
    resultImg.append(pygame.image.load(name))
    resultImg[i] = pygame.transform.scale(resultImg[i], (150, 75))

resultImgRec = resultImg[0].get_rect()
resultImgRec.centerx = SCREEN_WIDTH/2 - resultImgRec.width/2 - 40
resultImgRec.centery = targetArea.centery

while(isActive):
    screen.fill((255, 255, 255))
    eventProcess()
    drawIcon()
    setText()
    drawResult()
    pygame.display.update()
    clock.tick(250)