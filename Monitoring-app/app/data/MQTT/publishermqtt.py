import paho.mqtt.publish as publish
import time
import random

broker_address = "test.mosquitto.org"
broker_port = 1883
topic = "iot/esisa/test"

while True:

    device_id = "1"
    temperature = round(random.uniform(20.0, 30.0), 2)

  
    message = f'{{"device_id": "{device_id}", "temperature": {temperature}}}'
    
    publish.single(topic, message, hostname=broker_address, port=broker_port)

    print(f"Published: {message}")

    time.sleep(60)
    
    
    if __name__ == "__main__" :
        pass