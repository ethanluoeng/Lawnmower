import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

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

def move_backward(speed=50):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN1, True)
    GPIO.output(AIN2, False)

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, True)
    GPIO.output(BIN2, False)

def move_forward(speed=50):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN1, False)
    GPIO.output(AIN2, True)

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, False)
    GPIO.output(BIN2, True)

def turn_right(speed=50):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN1, False)
    GPIO.output(AIN2, True)

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, True)
    GPIO.output(BIN2, False)

def turn_left(speed=50):
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

# MQTT Callback
def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Received command: {command}")

    if command == "forward":
        move_forward()
    elif command == "backward":
        move_backward()
    elif command == "left":
        turn_left()
    elif command == "right":
        turn_right()
    elif command == "stop":
        stop()

# MQTT Setup
client = mqtt.Client()
client.on_message = on_message

broker_address = "192.168.10.111"  # Change this to your laptop's IP address
client.connect(broker_address, 1883)

client.subscribe("lawnmower/move")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    stop()
    GPIO.cleanup()
