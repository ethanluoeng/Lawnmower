import RPi.GPIO as GPIO
import time

pin = 32

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def Print(x):
    if x == 0:
        print('Magnetic field detected!')
    elif x == 1:
        print('No magnetic field')
    

def loop():
    sig = 0
    while True:
        currentSig = GPIO.input(pin)
        if sig != currentSig:
            Print(currentSig)
            sig = currentSig
        time.sleep(0.1)

def destroy():
    GPIO.cleanup
    
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()