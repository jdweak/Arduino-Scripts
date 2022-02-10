#-- ExternalLedBlink.py - CircuitPython code for CP --#
# Blink an external LED light wired through a bread board
# Import Section
import board
import digitalio
from time import sleep

# Setup Section
led = digitalio.DigitalInOut(board.A1)
led.direction = digitalio.Direction.OUTPUT

# Loop Section
while True:
  led.value = True
  sleep(0.5)
  led.value = False
  sleep(0.5)
