#spins lights in a circle
import time
from adafruit_circuitplayground import cp

counter = 0
prev = 0
cp.red_led = True

while True:
    cp.red_led = not cp.red_led
    if counter == 0:
        prev = 9
    else:
        prev = counter - 1
    cp.pixels[counter] = (50, 50, 0)
    cp.pixels[prev] = (0, 0, 0)
    counter = (counter + 1) % 10
    time.sleep(0.5)
