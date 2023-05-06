from paho.mqtt import client as mqtt_client

import time

mqttBrokerURL = "broker.hivemq.com"
mqttBrokerPort = 1883
topic = "img_sub/test_publisher/images"
client_id = "TestImagePublisher"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(mqttBrokerURL, mqttBrokerPort)
    return client

def publish(client: mqtt_client):
    with open("./test_images/image1.jpg",'rb') as file:
        filecontent = file.read()
        byteArr = bytearray(filecontent)
        print(byteArr)
        result = client.publish(topic,byteArr,2)
    msg_status = result[0]
    if msg_status == 0:
        print(f"message sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")

def main():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    time.sleep(5)
    client.loop_stop()
if __name__ == '__main__':
    main()

