#-- ExternalProximitySensorWithWarnings.py - CircuitPython code for CP --#

# Import Section
import board
from adafruit_circuitplayground import cp
from adafruit_hcsr04 import HCSR04
from time import sleep
from Queue import Queue
import adafruit_motor.servo
import pwmio


# Setup Section
led_brightness = 0.25
t = 0
dt = 0.1
sonar = HCSR04(trigger_pin=board.TX, echo_pin=board.A6)
cp.pixels.fill((255,0,0))
cp.pixels.brightness = 0
pwm = pwmio.PWMOut(board.A1, frequency=50)
servo = adafruit_motor.servo.Servo(pwm, min_pulse=750, max_pulse=2600)

#how many samples must be over the limit for it to be open
numOpenSampleThreshold = 10
#theshold for considering the door open based on averageDistance
openDistanceThreshold = 12
#is the door open
doorOpen = False
#counter of how many times the door has been open
doorOpenCounter = 0
#amount of snacks per day
snackLimit = 3
#amount of snacks left in current day
snacksLeft = snackLimit


# Function Section
def pixel_flip():
    if cp.pixels.brightness > 0:
        cp.pixels.brightness = 0
    else:
        cp.pixels.brightness = led_brightness
            
            
def openDoor():
    servo.angle = 0

def closeDoor():
    servo.angle = 180

openDoor()

# Loop Section
while True:
    try:
        #take the current distance point from door
        newDistance = sonar.distance
        

        if newDistance > openDistanceThreshold:
            doorOpenCounter += 1
            if doorOpenCounter == numOpenSampleThreshold:
                doorOpen = True
                cp.play_file("one-punch.wav")

        else:
            doorOpenCounter = 0
            if doorOpen == True:
                doorOpen = False
                snacksLeft -= 1
            if(snacksLeft == 0):
                closeDoor()
    
        print('door open counter: ', doorOpenCounter)
        print('door open t/f: ', doorOpen)
        print('snacks left: ', snacksLeft)
        
    except RuntimeError:
        print("Retrying!")
    sleep(dt)
