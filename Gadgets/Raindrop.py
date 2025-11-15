import RPi.GPIO as GPIO
import PCF8591 as ADC #import the PCF8591 script as a module
import time
import math

DO = 17
GPIO.setmode(GPIO.BCM)

def setup():
    GPIO.setup(DO, GPIO.IN)
    ADC.setup(0x48)

def Print(x):
    if x == 0:
        print('')
        print('***********')
        print("* I'm wet *")
        print('***********')
        print('')

    elif x == 1:
        print('')
        print('***************')
        print("* I'm not wet *")
        print('***************')
        print('')


def loop():    
    status = 1
    
    while True:
        print(ADC.read(0))
        curr = GPIO.input(DO)
        
        if status != curr:
            Print(curr)
            status = curr
        
        time.sleep(0.1)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup()
        loop()
    
    except KeyboardInterrupt:
        destroy()
