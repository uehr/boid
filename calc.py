import random
import numpy as np
import math

def randomColor():
    b = random.randrange(255)
    g = random.randrange(255)
    r = random.randrange(255)

    return [b, g, r]


def lineEquation(point1, point2):
    y = [point1[0], point2[0]]
    x = [point1[1], point2[1]]
    fited = np.polyfit(x, y, 1)

    return fited


def pt2ToDeg(point1, point2):
    y1, x1 = point1
    y2, x2 = point2

    changeInX = x2 - x1
    changeInY = y2 - y1

    return math.degrees(math.atan2(changeInY, changeInX))


def pointsAverage(points):
    ySum = 0
    xSum = 0
    pointsCnt = len(points)

    for pt in points:
        y, x = pt
        ySum += y
        xSum += x

    yAve = int(ySum / pointsCnt)
    xAve = int(xSum / pointsCnt)

    return yAve, xAve



def distance2Pt(point1, point2):
    y1, x1 = point1
    y2, x2 = point2

    return np.sqrt((x2-x1)**2 + (y2-y1)**2)