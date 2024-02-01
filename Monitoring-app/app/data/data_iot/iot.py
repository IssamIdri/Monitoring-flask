import paho.mqtt.client as mqtt
import random
import time, json

MQTT_BROKER_URL = 'test.mosquitto.org'
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = 'iot/esisa'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connection established')
        client.subscribe(MQTT_TOPIC)
        # Add this line to publish a test message immediately after connecting
        client.publish(MQTT_TOPIC, 'Test message')
    else:
        print('Connection refused')

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT)

client.loop_start()

try:
    while True:
        temperature = round(random.uniform(10, 42), 6)
        payload = {'temperature': temperature}
        client.publish(MQTT_TOPIC, json.dumps(payload))
        print('Temperature:', temperature)
        time.sleep(10)
except Exception as e:
    print('error', e)
    client.disconnect()

