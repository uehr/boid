import world
from fish import fish
import cv2

world = world.world(1920, 1080)

for _ in range(20):
    world.addLife(fish)

while True:
    worldImg = world.draw()
    world.advanceTime(speedScale=2)
    cv2.imshow("boid", worldImg)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cv2.destroyAllWindows()