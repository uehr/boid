def getLife(lifes, targetId):
    for life in lifes:
        if life.id == targetId:
            return life
            lifes.remove(life)


def removeLife(lifes, targetId):
    targetLife = getLife(lifes, targetId)
    lifes.remove(targetLife)