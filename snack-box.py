#-- ExternalProximitySensorWithWarnings.py - CircuitPython code for CP --#

# Import Section
import board
from adafruit_circuitplayground import cp
from adafruit_hcsr04 import HCSR04
from time import sleep
from queue import Queue

# Setup Section
led_brightness = 0.25
t = 0
dt = 0.25
sonar = HCSR04(trigger_pin=board.TX, echo_pin=board.A6)
cp.pixels.fill((255,0,0))
cp.pixels.brightness = 0

#how many past samples to consider in the running average
sampleRangeSize = 100
#queue to store most recent distance data points
distanceData = Queue(sampleRangeSize)
#measured distance between closed door and sensor
doorDistance = 10
#sum of distance points in the distanceData queue
totalDistance = doorDistance
#average of distance points in the distanceData queue
averageDistance = doorDistance
#theshold for considering the door open based on averageDistance
openDistanceThreshold = 12

# Function Section
def pixel_flip():
    if cp.pixels.brightness > 0:
        cp.pixels.brightness = 0
    else:
        cp.pixels.brightness = led_brightness
            

def initializeQueue():
    for i in range(sampleRangeSize):
        distanceData.put(doorDistance)
        

#Initialize section
initializeQueue()

# Loop Section
while True:
    try:
        #take the current distance point from door
        newDistance = sonar.distance
        #update the average distance and distance data queue
        totalDistance = totalDistance - distanceData.get()
        totalDistance = totalDistance + newDistance
        distanceData.put(newDistance)
        averageDistance = totalDistance / distanceData.qsize()
        
        print('average distance: ', averageDistance)
        
        
        # Closer than 15 cm is Dangerously Close
        if averageDistance >= openDistanceThreshold:
            pixel_flip()
            if t >= 1.0:
                cp.play_tone(440, 0.25)
                t = 0
    except RuntimeError:
        print("Retrying!")
    sleep(dt)
