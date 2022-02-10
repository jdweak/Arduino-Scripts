#-- ExternalBuzzerDirect.py - CircuitPython code for CPX --#
# Use external buzzer connected through breadboard

# Import Section
import board
import pwmio
from time import sleep

# Setup Section
buzzer = pwmio.PWMOut(board.A1, variable_frequency=True)
buzzer.frequency = 440 # This is an A3
OFF = 0
ON = 2**15
# Loop Section
while True:
    buzzer.duty_cycle = ON
    sleep(1.0)
    buzzer.duty_cycle = OFF
    sleep(2.0)
