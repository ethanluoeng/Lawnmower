import paho.mqtt.client as mqtt
import time

broker = "63f7d02512c948328feb80c8075ba227.s1.eu.hivemq.cloud"
port = 8883
username = "ethan"
password = "Summer2025!"
topic = "robot/control"

# Create client using protocol v3.1.1
client = mqtt.Client(client_id="laptop-client", protocol=mqtt.MQTTv311)

client.username_pw_set(username, password)
client.tls_set()

# Connect and wait
client.connect(broker, port)
client.loop_start()  # Non-blocking background loop

time.sleep(1)  # Ensure connection completes

result = client.publish(topic, payload="forward", qos=1, retain=True)
print("Publish result code:", result.rc)  # Should be 0

time.sleep(1)  # Give time to send before disconnecting
client.loop_stop()
client.disconnect()
