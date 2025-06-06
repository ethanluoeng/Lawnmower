import paho.mqtt.client as mqtt
import keyboard
import time

broker = "63f7d02512c948328feb80c8075ba227.s1.eu.hivemq.cloud"
port = 8883
username = "ethan"
password = "Summer2025!"
topic = "robot/control"

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(username, password)
client.tls_set()
client.connect(broker, port)
client.loop_start()

command = None

while True:
    if keyboard.is_pressed('w'):
        if keyboard.is_pressed('a'):
            command = "f_left"
        elif keyboard.is_pressed('d'):
            command = "f_right"
        else:
            command = "forward" 

    elif keyboard.is_pressed('s'):
        if keyboard.is_pressed('a'):
            command = "b_left"
        elif keyboard.is_pressed('d'):
            command = "b_right"
        else:
            command = "backward"
    else:
        command = "stop"
    client.publish(topic, command, qos=1)
    time.sleep(0.3)
client.loop_stop()
client.disconnect()

