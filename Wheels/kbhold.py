import RPi.GPIO as GPIO
import time
import keyboard

# Pin setup
PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 100)
R_Motor = GPIO.PWM(PWMB, 100)
L_Motor.start(0)
R_Motor.start(0)

def move_backward(speed=75):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN1, True)
    GPIO.output(AIN2, False)

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, True)
    GPIO.output(BIN2, False)

def move_forward(speed=75):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN1, False)
    GPIO.output(AIN2, True)

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, False)
    GPIO.output(BIN2, True)

def turn_right(speed=75):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN1, False)
    GPIO.output(AIN2, True)

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, True)
    GPIO.output(BIN2, False)

def turn_left(speed=75):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN1, True)
    GPIO.output(AIN2, False)

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, False)
    GPIO.output(BIN2, True)

def stop():
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN1, False)
    GPIO.output(AIN2, False)

    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN1, False)
    GPIO.output(BIN2, False)

print("Use W/A/S/D to move. Q to quit.")

try:
    while True:
        stop()
        while keyboard.is_pressed('w'):
            move_forward()
        while keyboard.is_pressed('s'):
            move_backward()
        while keyboard.is_pressed('a'):
            turn_left()
        while keyboard.is_pressed('d'):
            turn_right()
        if keyboard.is_pressed('q'):
            stop()
            break
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    stop()
    GPIO.cleanup()
    print("Program ended and GPIO cleaned up.")