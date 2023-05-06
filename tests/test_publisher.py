from paho.mqtt import client as mqtt_client

from uuid import uuid4
from typing import NewType, Callable

import sys
import time


def _on_connect_default(rc):
    if rc == 0:
        print('connected successfully')
    else:
        print(f'failed to connect with code {rc}')


ConnectCallback = NewType('ConnectCallback', Callable[[int], None])


class MqttTestPublisher:
    def __init__(self, broker_url: str, broker_port: int, on_connect: ConnectCallback = _on_connect_default):
        self._client = self._connect_mqtt(
            broker_url, broker_port, on_connect)

    def publish(self, topic: str, msg: str):
        self._client.loop_start()
        result = self._client.publish(topic, msg, 2)
        self._client.loop_stop()
        return result

    def _connect_mqtt(self, broker_url, broker_port, on_connect):
        client = mqtt_client.Client(str(uuid4()))
        client.on_connect = self._wrap_on_connect(on_connect)
        client.connect(broker_url, broker_port)
        client.loop_start()
        time.sleep(1)
        client.loop_stop()
        return client

    def _wrap_on_connect(self, on_connect):
        def _on_connect(client, userdata, flags, rc):
            on_connect(rc)
        return _on_connect


def main(broker_url, broker_port, topic, msg):
    publisher = MqttTestPublisher(broker_url, broker_port)
    result = publisher.publish(topic, msg)

    if result[0] == 0:
        print(f'message sent to topic {topic}')
    else:
        print(f'Failed to send message to topic {topic}')


if __name__ == '__main__':
    broker_url = sys.argv[1]
    broker_port = int(sys.argv[2])
    topic = sys.argv[3]
    msg = sys.argv[4]
    main(broker_url, broker_port, topic, msg)
