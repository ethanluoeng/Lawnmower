import RPi.GPIO as GPIO
import time

pin = 32

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def loop():
    sig = 0
    a = 0
    while True:
        currentSig = GPIO.input(pin)
        if sig != currentSig:
            a += 1
            print('vibrating!!!' + str(a))
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