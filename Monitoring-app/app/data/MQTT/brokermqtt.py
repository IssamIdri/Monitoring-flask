import paho.mqtt.client as mqtt
import json
from app.data.IOTservice.iotservice import iotdevice

class TemperatureReceiver:
    iot_device = iotdevice()

    def __init__(self, custom_topic, mqtt_broker="test.mosquitto.org", mqtt_port=1883):
        self.custom_topic = custom_topic
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def connect(self):
        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f'Connected to MQTT broker for topic: {self.custom_topic}')
            client.subscribe(self.custom_topic)
        else:
            print(f'Failed to connect to MQTT broker with code {rc}')

    def handle_temperature(self, id, temp):
        self.iot_device.add_iotdevice_inforamtion(Mac=id, temperature_values=temp)

    def on_message(self, client, userdata, message):
        if message.topic == self.custom_topic:
            payload = message.payload.decode()
            try:
                data = json.loads(payload)
                device_id = data.get("idd")
                temperature = data.get("temp")
                self.handle_temperature(device_id, temperature)
                print(f"Received MQTT Message: Device ID: {device_id}, Temperature: {temperature}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON payload: {e}")


if __name__ == "__main__":
    pass
