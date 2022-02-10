#every .5 seconds switch a random amount of lights to a random color
import time
import random
from adafruit_circuitplayground import cp

counter = 0
prev = 0
cp.red_led = True
cp.pixels.brightness = 0.1


while True:
    cp.red_led = not cp.red_led

    for i in range(9):
        if random.random() > .35:
            cp.pixels[i] = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))
        else:
            cp.pixels[i] = (0, 0, 0)
    time.sleep(0.5)
