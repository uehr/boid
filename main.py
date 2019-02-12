import world
from bard import bard
import cv2

world = world.world(480, 270)

for _ in range(15):
    world.addLife(bard)

while True:
    worldImg = world.draw()
    world.advanceTime(speedScale=2)
    cv2.imshow("boid", worldImg)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cv2.destroyAllWindows()