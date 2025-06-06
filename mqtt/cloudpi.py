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

def on_message(client, userdata, msg):
    print(f"Message received on topic: {msg.topic}")
    command = msg.payload.decode()
    print(f"Received command: {command}")

    if command == "forward":
        print("Moving forward")
    elif command == "stop":
        print("Stopping")

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(username, password)
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_forever()
