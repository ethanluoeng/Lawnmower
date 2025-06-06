import paho.mqtt.client as mqtt

broker = "63f7d02512c948328feb80c8075ba227.s1.eu.hivemq.cloud"
port = 8883
username = "ethan"
password = "Summer2025!"
topic = "robot/control"

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(username, password)
client.tls_set()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    # This will publish an empty retained message and remove it from the broker
    result = client.publish(topic, payload="", qos=1, retain=True)
    print("Clearing retained message:", result.rc)

client.on_connect = on_connect

client.connect(broker, port)
client.loop_start()

import time
time.sleep(2)  # Give it time to connect and send

client.loop_stop()
client.disconnect()
