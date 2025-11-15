import RPi.GPIO as GPIO
import time

pin = 32

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def Print(x):
    if x == 0:
        print('Tilted upwards')
    elif x == 1:
        print('Tilted downwards')

def loop():
    pinValue = 1
    while True:
        currentValue = GPIO.input(pin)
        if currentValue != pinValue:
            pinValue = currentValue
            Print(pinValue)
        time.sleep(0.1)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()   