import numpy as np
import random
import uuid
import calc

class invalidPointError(Exception): pass


class baseLife:
    def __init__(self, worldHeight, worldWidth, spawnY, spawnX):
        self.worldHeight = worldHeight
        self.worldWidth = worldWidth
        self.point = (spawnY, spawnX)
        self.id = str(uuid.uuid4())


    def isOutsideWorld(self, point):
        y,x = point

        if y > self.worldHeight-1: return True
        elif y < 0: return True
        elif x > self.worldWidth-1: return True
        elif x < 0: return True

        return False


    def nearNextPoint(self, point):
        y, x = self.point
        toY, toX = point

        if toY == y:
            if toX > x: nextPt = self.rightPt()
            else: nextPt = self.leftPt()
        elif toX == x:
            if toY > y: nextPt = self.downPt()
            else: nextPt = self.upPt()
        elif toX > x and toY > y:
            nextPt = self.rightDownPt()
        elif toX > x and toY < y:
            nextPt = self.rightUpPt()
        elif toX < x and toY > y:
            nextPt = self.leftDownPt()
        elif toX < x and toY < y:
            nextPt = self.leftUpPt()
        else: raise invalidPointError()

        return nextPt


    def distance(self, point):
        return calc.distance2Pt(self.point, point)


    def move(self, point):
        if self.isOutsideWorld(point): raise invalidPointError()
        self.point = point

    
    def allNextPts(self):
        return [self.leftUpPt(), self.upPt(), self.rightUpPt(), self.leftPt(), self.rightPt(), self.leftDownPt(), self.downPt(), self.rightDownPt()]


    def randomNextPt(self):
        nextPt = random.choice(self.allNextPts())
        return nextPt


    def upPt(self):
        y,x = self.point
        return (y-1, x)


    def leftUpPt(self):
        y,x = self.point
        return (y-1, x-1)


    def rightUpPt(self):
        y,x = self.point
        return (y-1, x+1)


    def leftPt(self):
        y,x = self.point
        return (y, x-1)


    def rightPt(self):
        y,x = self.point
        return (y, x+1)


    def downPt(self):
        y,x = self.point
        return (y+1, x)


    def leftDownPt(self):
        y,x = self.point
        return (y+1, x-1)


    def rightDownPt(self):
        y,x = self.point
        return (y+1, x+1)