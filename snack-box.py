# Import Section
import board
from adafruit_circuitplayground import cp
from adafruit_hcsr04 import HCSR04
from time import sleep
from Queue import Queue
import adafruit_motor.servo
import pwmio
import digitalio


# Setup Section

#connect to sonar and servo motor
sonar = HCSR04(trigger_pin=board.TX, echo_pin=board.A6)
pwm = pwmio.PWMOut(board.A1, frequency=50)
servo = adafruit_motor.servo.Servo(pwm, min_pulse=750, max_pulse=2600)

#led lights setup. the numbers after the led represents the
#light that should be on when that many snacks are left
led_brightness = 0.25
ledDoor = digitalio.DigitalInOut(board.A2)
ledDoor.direction = digitalio.Direction.OUTPUT
ledDoor.value = False
led3 = digitalio.DigitalInOut(board.A3)
led3.direction = digitalio.Direction.OUTPUT
led3.value = True
led2 = digitalio.DigitalInOut(board.A4)
led2.direction = digitalio.Direction.OUTPUT
led2.value = True
led1 = digitalio.DigitalInOut(board.A5)
led1.direction = digitalio.Direction.OUTPUT
led1.value = True

#Script Variables Setup

#running time of program
t = 0.0
#time between loops of program
dt = 0.1
#variable for how long to sleep (calculated later in script)
sleepTime = 0.0
#how many samples must be over the limit for it to be open
numOpenSampleThreshold = 5
#theshold for considering the door open based on averageDistance
openDistanceThreshold = 9
#is the door open
doorOpen = False
#counter of how many times the door has been open
doorOpenCounter = 0
#amount of snacks per day
snackLimit = 3
#amount of snacks left in current day
snacksLeft = snackLimit
#How long in seconds there is between a reset of snacksLeft (default 24 hours)
resetInterval = 40

# Function Section
def pixel_flip():
    if cp.pixels.brightness > 0:
        cp.pixels.brightness = 0
    else:
        cp.pixels.brightness = led_brightness


def openDoor():
    servo.angle = 0

def closeDoor():
    servo.angle = 90

#reset all values to full after a new interval has passed
def resetHardware():
    openDoor()
    led3.value = True
    led2.value = True
    led1.value = True

# Loop Section
while True:
    try:
        print('mod value: ', t % resetInterval)
        #when the time is on the reset time, reset all variables to beginning of day values
        if round((t % resetInterval), 1) == 0.1:
            resetHardware()
            snacksLeft = snackLimit
            print('reseting')

        #take the current distance point from door
        newDistance = sonar.distance

        #if the door is determined to be open
        if newDistance > openDistanceThreshold:
            doorOpenCounter += 1
            if doorOpenCounter == numOpenSampleThreshold:
                doorOpen = True
            if doorOpenCounter > numOpenSampleThreshold * 5 and doorOpenCounter % 20 == 0:
                t += .3
                cp.play_tone(3200, 0.3)
                ledDoor.value = not ledDoor.value
        #the door is closed
        else:
            doorOpenCounter = 0
            ledDoor.value = False
            if doorOpen == True:
                doorOpen = False
                snacksLeft -= 1
            if snacksLeft == 2:
                led3.value = False
            elif snacksLeft == 1:
                led2.value = False
            elif snacksLeft == 0:
                led1.value = False
                closeDoor()
                sleepTime = resetInterval - (t % resetInterval)
                t += sleepTime
                sleep(sleepTime)

        print('door open counter: ', doorOpenCounter)
        print('door open t/f: ', doorOpen)
        print('snacks left: ', snacksLeft)
#        print('time: ', t)

    except RuntimeError:
        print("Retrying!")
    t += dt
    t = round(t, 1)
    sleep(dt)
