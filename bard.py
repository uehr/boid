import warnings
warnings.filterwarnings('ignore')
from scipy import ndimage
import numpy as np
import baseLife
import calc
import cv2
import random

# v1: toCenterMoveAmount
# v2: avoidBardsMoveAmount
# v3: nearBardsAverageMoveAmount

class bard(baseLife.baseLife):
    def __init__(self, worldHeight, worldWidth, spawnY, spawnX, r1=0.9, r2=0.5, r3=0.5, maxSpeed=15, sizePx=30):
        super().__init__(worldHeight, worldWidth, spawnY, spawnX)
        self.otherBards = []
        self.type = "bard"

        self.vx = random.randrange(maxSpeed*-1, maxSpeed)
        self.vy = random.randrange(maxSpeed*-1, maxSpeed)

        self.r1 = r1
        self.r2 = r2
        self.r3 = r3

        self.sizePx = sizePx

        self.color = [150, 0, 0]
        self.maxSpeed = maxSpeed


    def draw(self, img, tailLength=3):
        tailPoint = self.point[0] + int(self.vy) * tailLength * -1, self.point[1] + int(self.vx) * tailLength * -1
        img = cv2.circle(img, self.point, self.sizePx, self.color, -1)
        img = cv2.line(img, self.point, tailPoint, self.color, 30)

        return img


    def randomMoveAmount(self):
        moveY = random.randrange(self.maxSpeed*-1, self.maxSpeed)
        moveX = random.randrange(self.maxSpeed*-1, self.maxSpeed)

        return (moveY, moveX)


    def avoidEnemyMoveAmount(self):
        moveY = 0
        moveX = 0
        selfY, selfX = self.point

        for enemy in self.enemys:
            y,x = enemy.point

            if self.distance(enemy.point) < self.sizePx*2.5:
                moveY -= y - selfY
                moveX -= x - selfX

        return int(moveY), int(moveX)


    def toCenterMoveAmount(self, CENTER_PULL_FACTOR=80):
        moveX = 0
        moveY = 0
        selfY, selfX = self.point

        for bard in self.otherBards:
            y,x = bard.point
            moveY += y
            moveX += x

        moveY /= len(self.otherBards)
        moveX /= len(self.otherBards)

        moveX = (moveX - selfX) / CENTER_PULL_FACTOR
        moveY = (moveY - selfY) / CENTER_PULL_FACTOR

        return int(moveY), int(moveX)


    def avoidBardsMoveAmount(self):
        moveY = 0
        moveX = 0
        selfY, selfX = self.point

        for bard in self.otherBards:
            y,x = bard.point

            if self.distance(bard.point) < self.sizePx*2.5:
                moveY -= y - selfY
                moveX -= x - selfX

        return int(moveY), int(moveX)


    def avoidEdgeMoveAmount(self, DIST_THRESHOLD=100):
        moveY = 0
        moveX = 0
        selfY, selfX = self.point

        if selfX < DIST_THRESHOLD:
            moveX += (DIST_THRESHOLD - selfX)

        if selfY < DIST_THRESHOLD:
            moveY += (DIST_THRESHOLD - selfY)

        if selfX > self.worldWidth - DIST_THRESHOLD:
            moveX += (selfX - self.worldWidth - DIST_THRESHOLD)

        if selfY > self.worldHeight - DIST_THRESHOLD:
            moveY += (selfY - self.worldHeight - DIST_THRESHOLD)

        return int(moveY * 2), int(moveX * 2)


    def nearBardsAverageMoveAmount(self):
        moveY = 0
        moveX = 0

        for bard in self.otherBards:
            moveY += bard.vy
            moveX += bard.vx

        moveY /= len(self.otherBards)
        moveX /= len(self.otherBards)

        return int(moveY), int(moveX)


    def next(self, otherLifes):
        avoidEdgeDis = 50

        self.otherBards = list(filter(lambda life: life.type == "bard", otherLifes))
        selfY, selfX = self.point

        v1 = self.toCenterMoveAmount()
        v2 = self.avoidBardsMoveAmount()
        v3 = self.nearBardsAverageMoveAmount()

        v1 = (v1[0]/self.r1, v1[1]/self.r1)
        v2 = (v2[0]/self.r2, v2[1]/self.r2)
        v3 = (v3[0]/self.r3, v3[1]/self.r3)

        vy = v1[0] + v2[0] + v3[0]
        vx = v1[1] + v2[1] + v3[1]

        if vy != 0 and vx != 0:
            self.vy = vy
            self.vx = vx

        #self.vy += random.randrange(-1, 1)
        #self.vx += random.randrange(-1, 1)

        if self.vy > 0 and self.vy < 1: self.vy = 1
        if self.vx > 0 and self.vx < 1: self.vx = 1

        if self.vy > -1 and self.vy < 0: self.vy = -1
        if self.vx > -1 and self.vx < 0: self.vx = -1

        movement = np.sqrt(self.vy * self.vy + self.vx * self.vx)
        if movement > self.maxSpeed:
            self.vy = (self.vy / movement) * self.maxSpeed
            self.vx = (self.vx / movement) * self.maxSpeed

        nextY = selfY + int(self.vy)
        nextX = selfX + int(self.vx)

        avoidEdgeScale = 2

        if nextY < 0:
            nextY = 0
            self.vy *= avoidEdgeScale * -1

        if nextX < 0:
            nextX = 0
            self.vx *= avoidEdgeScale * -1

        if nextY > self.worldHeight-1:
            nextY = self.worldHeight-1
            self.vy *= avoidEdgeScale * -1

        if nextX > self.worldWidth-1:
            nextX = self.worldWidth-1
            self.vx *= avoidEdgeScale * -1

        nextPoint = (nextY, nextX)
        self.move(nextPoint)