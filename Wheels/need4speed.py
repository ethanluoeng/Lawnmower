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

def left_backward(l_speed):
    L_Motor.ChangeDutyCycle(l_speed)
    GPIO.output(AIN1, True)
    GPIO.output(AIN2, False)

def right_backward(r_speed):
    R_Motor.ChangeDutyCycle(r_speed)
    GPIO.output(BIN1, True)
    GPIO.output(BIN2, False)

def left_forward(l_speed):
    L_Motor.ChangeDutyCycle(l_speed)
    GPIO.output(AIN1, False)
    GPIO.output(AIN2, True)

def right_forward(r_speed):
    R_Motor.ChangeDutyCycle(r_speed)
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

speed = 0
speed_step = 10
speed_break = 5
max_speed = 80
min_speed = 0
direction = None

try:
    while True:
        
        while speed > 0:
            speed = max(0, speed - speed_break)
            if direction == "forward":
                left_forward(speed)
                right_forward(speed)
            elif direction == "backward":
                left_backward(speed)
                right_backward(speed)
            
            if keyboard.is_pressed('space'):
                speed = max(0, speed - speed_step)
            time.sleep(0.2)        
            
        while keyboard.is_pressed('w'):
            direction = "forward"
            while keyboard.is_pressed('a'):
                speed = min(max_speed, speed + speed_step)
                left_forward(0)
                right_forward(speed)
                time.sleep(0.4)
            while keyboard.is_pressed('d'):
                speed = min(max_speed, speed + speed_step)
                left_forward(speed)
                right_forward(0)
                time.sleep(0.4)
            speed = min(max_speed, speed + speed_step)
            left_forward(speed)
            right_forward(speed)
            time.sleep(0.2)
        
        while keyboard.is_pressed('s'):
            direction = "backward"
            while keyboard.is_pressed('a'):
                speed = min(max_speed, speed + speed_step)
                left_backward(0)
                right_backward(speed)
                time.sleep(0.4)
            while keyboard.is_pressed('d'):
                speed = min(max_speed, speed + speed_step)
                left_backward(speed)
                right_backward(0)
                time.sleep(0.4)
            speed = min(max_speed, speed + speed_step)
            left_backward(speed)
            right_backward(speed)
            time.sleep(0.2)

except KeyboardInterrupt:
    pass
finally:
    stop()
    GPIO.cleanup()
    print("Program ended and GPIO cleaned up.")
