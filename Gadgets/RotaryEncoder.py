import RPi.GPIO as GPIO

APin = 11    # CLK Pin
BPin = 12

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(APin, GPIO.IN)
    GPIO.setup(BPin, GPIO.IN)

    
    