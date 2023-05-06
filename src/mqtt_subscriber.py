from paho.mqtt import client as mqtt_client, MQTTMessage
import uuid
from typing import NewType, Callable, Any, Dict


class MutableFlag:
    def __init__(self, value: bool):
        self.value = value


ConnectCallback = NewType(
    '_', Callable[[mqtt_client, Any, Dict[str, Any], int], None])


def _on_connect_default(client, userdata, flags, rc):
    if rc == 0:
        print('connected successfully')
    else:
        print(f'failed to connect with code {rc}')


class MqttSubscriber:
    def __init__(self, broker_url: str, broker_port: int, id: str = str(uuid.uuid4()), on_connect: ConnectCallback = _on_connect_default):
        self._client = self._connect_mqtt(
            broker_url, broker_port, id, on_connect)

    def subscribe(topic: str, on_message_callback):
        def on_message(self.client, userdata, msg):
            f = open('receive.jpg', 'wb')
            f.write(msg.payload)
            f.close()
            print('image received')
        self.client.subscribe(topic)
        self.client.on_message = on_message

    def _connect_mqtt(self, broker_url, broker_port, id, connect_callback):
        client = mqtt_client.Client(id)
        self._connect_blocking(client, broker_url, broker_port,
                               connect_callback)
        return client

    def _connect_blocking(self, client, broker_url, broker_port, connect_callback):
        connect_flag = MutableFlag(False)
        client.on_connect = self._create_blocking_callback(
            connect_callback, connect_flag)
        client.connect(broker_url, broker_port)
        self._wait_on_callback(client, connect_flag)

    def _create_blocking_callback(self, connect_callback, connect_flag):
        def blocking_callback(client, userdata, flags, rc):
            connect_flag.value = True
            connect_callback(client, userdata, flags, rc)
        return blocking_callback

    def _wait_on_callback(self, client, connect_flag):
        client.loop_start()
        while not connect_flag.value:
            pass
        client.loop_stop()


def main():  # todo: write this with input arguments so it can be used by test_pub
    mqttBrokerURL = 'broker.hivemq.com'
    mqttBrokerPort = 1883
    topic = 'img_sub/test_publisher/images'
    client_id = 'ImageReceiver'
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    main()
