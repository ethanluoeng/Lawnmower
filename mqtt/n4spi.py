import paho.mqtt.client as mqtt 

broker = "63f7d02512c948328feb80c8075ba227.s1.eu.hivemq.cloud"
port = 8883
username = "ethan"
password = "Summer2025!"
topic = "robot/control"

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with code", rc)
    if rc == 0:
        print("Connection successful!")
        result, _ = client.subscribe(topic, qos=1)
        print("Subscribe result code:", result)
    else:
        print("Connection failed!")

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

l_speed = 0
r_speed = 0
speed_step = 10
max_speed = 80
direction = None

def on_message(client, userdata, msg):
    global l_speed, r_speed, direction  #declare global variable
    command = msg.payload.decode()
    print(f"Received command: {command}")
    
    if command in ["forward", "f_left", "f_right"]:
        if direction == "backward":
            while l_speed > 0 or r_speed > 0:
                l_speed = max(0, l_speed - 20)
                r_speed = max(0, r_speed - 20)
                left_backward(l_speed)
                right_backward(r_speed)
                time.sleep(0.3)
            direction = "forward"
        else:
            direction = "forward"
            
            if command == "forward":
                l_speed = min(max_speed, l_speed + speed_step)
                r_speed = min(max_speed, r_speed + speed_step)
                left_forward(l_speed)
                right_forward(r_speed)
            
            elif command == "f_left":
                l_speed = max(0, l_speed - speed_step)
                r_speed = min(max_speed, r_speed + speed_step)
                left_forward(l_speed)
                right_forward(r_speed)
    
            elif command == "f_right":
                l_speed = min(max_speed, l_speed + speed_step)
                r_speed = max(0, r_speed - speed_step)
                left_forward(l_speed)
                right_forward(r_speed)
    
    if command in ["backward", "b_left", "b_right"]:
        if direction == "forward":
            while l_speed > 0 or r_speed > 0:
                l_speed = max(0, l_speed - 20)
                r_speed = max(0, r_speed - 20)
                left_forward(l_speed)
                right_forward(r_speed)
                time.sleep(0.3)
            direction = "backward"
        else:
            direction = "backward"
            
            if command == "backward":
                l_speed = min(max_speed, l_speed + speed_step)
                r_speed = min(max_speed, r_speed + speed_step)
                left_backward(l_speed)
                right_backward(r_speed)
            elif command == "b_left":
                l_speed = max(0, l_speed - speed_step)
                r_speed = min(max_speed, r_speed + speed_step)
                left_backward(l_speed)
                right_backward(r_speed)
            elif command == "b_right":
                l_speed = min(max_speed, l_speed + speed_step)
                r_speed = max(0, r_speed - speed_step)
                left_backward(l_speed)
                right_backward(r_speed)
    
    if command == "stop":
        l_speed = max(0, l_speed - speed_step)
        r_speed = max(0, r_speed - speed_step)
        if direction == "forward":
            left_forward(l_speed)
            right_forward(r_speed)
        elif direction == "backward":
            left_backward(l_speed)
            right_backward(r_speed)
            
        #elif command == "stop":
            #print("Stopping")
            #stop()

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(username, password)
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_forever()
