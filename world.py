import cv2
import uuid
import random
import numpy as np
import matplotlib.pyplot as plt
from lifeListUtil import getLife, removeLife
from time import sleep


class world:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.time = 0
        self.lifes = []


    def randomPoint(self):
        randWidth = random.randrange(self.width)
        randHeight = random.randrange(self.height)

        return (randHeight, randWidth)


    def noOverlapRandomPoint(self):
        while True:
            point = self.randomPoint()
            if not self.isOverlapLife(point): return point


    def isOverlapLife(self, point):
        for life in self.lifes:
            if point == life.point: return True

        return False


    def addLife(self, lifeClass):
        # generate random spawn point
        spawnPoint = self.noOverlapRandomPoint()

        # spawn life
        life = lifeClass(self.height, self.width, spawnPoint[0], spawnPoint[1])
        self.lifes.append(life)

        return life.id


    def advanceTime(self, speedScale=1):
        self.time += 1

        for life in self.lifes:
            otherLifes = list(self.lifes)
            removeLife(otherLifes, life.id)
            life.next(otherLifes)

        if speedScale > 1:
            self.advanceTime(speedScale=speedScale-1)


    def draw(self):
        # create empty world
        worldImg = np.ones((self.width, self.height, 3), np.uint8) * 255

        # draw lifes on world
        for life in self.lifes:
            worldImg = life.draw(worldImg)
            sleep(0.00001)

        return worldImg