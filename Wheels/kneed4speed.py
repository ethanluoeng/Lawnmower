import RPi.GPIO as GPIO
import time
import keyboard

# --- Pin setup ---
PWMA = 18
AIN1 = 22
AIN2 = 27
PWMB = 23
BIN1 = 25
BIN2 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([AIN1, AIN2, PWMA, BIN1, BIN2, PWMB], GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 100)
R_Motor = GPIO.PWM(PWMB, 100)
L_Motor.start(0)
R_Motor.start(0)

# --- Motor Control ---
def set_motor(direction, l_speed, r_speed):
    if direction == "forward":
        GPIO.output(AIN1, False)
        GPIO.output(AIN2, True)
        GPIO.output(BIN1, False)
        GPIO.output(BIN2, True)
    elif direction == "backward":
        GPIO.output(AIN1, True)
        GPIO.output(AIN2, False)
        GPIO.output(BIN1, True)
        GPIO.output(BIN2, False)
    else:
        GPIO.output([AIN1, AIN2, BIN1, BIN2], False)

    L_Motor.ChangeDutyCycle(l_speed)
    R_Motor.ChangeDutyCycle(r_speed)

def stop():
    set_motor(None, 0, 0)

# --- Motion State ---
l_speed = 0
r_speed = 0
speed_step = 10
max_speed = 80
direction = None

print("Use W/A/S/D to move. Q to quit.")

try:
    while True:
        w = keyboard.is_pressed('w')
        s = keyboard.is_pressed('s')
        a = keyboard.is_pressed('a')
        d = keyboard.is_pressed('d')


        # Determine desired direction
        new_direction = "forward" if w else "backward" if s else None

        # If switching direction, decelerate to zero first
        if direction and new_direction and direction != new_direction:
            while l_speed > 0 or r_speed > 0:
                l_speed = max(0, l_speed - speed_step)
                r_speed = max(0, r_speed - speed_step)
                set_motor(direction, l_speed, r_speed)
                time.sleep(0.1)
            direction = None

        # Update current direction
        if new_direction:
            direction = new_direction

        # Accelerate if holding movement keys
        if w or s:
            if a:  # turn left
                l_speed = max(0, l_speed - speed_step)
                r_speed = min(max_speed, r_speed + speed_step)
            elif d:  # turn right
                l_speed = min(max_speed, l_speed + speed_step)
                r_speed = max(0, r_speed - speed_step)
            else:  # go straight
                l_speed = min(max_speed, l_speed + speed_step)
                r_speed = min(max_speed, r_speed + speed_step)

            set_motor(direction, l_speed, r_speed)

        else:
            # No movement key pressed → decelerate both motors
            if l_speed > 0 or r_speed > 0:
                if keyboard.is_pressed('space'):
                    l_speed = max(0, l_speed - speed_step)
                    r_speed = max(0, r_speed - speed_step)
                l_speed = max(0, l_speed - speed_step)
                r_speed = max(0, r_speed - speed_step)
                set_motor("forward" if direction == "forward" else "backward", l_speed, r_speed)
                time.sleep(0.2)
            else:
                stop()

        if keyboard.is_pressed('q'):
            break

        time.sleep(0.1)

except KeyboardInterrupt:
    pass
finally:
    stop()
    GPIO.cleanup()
    print("Program ended and GPIO cleaned up.")
