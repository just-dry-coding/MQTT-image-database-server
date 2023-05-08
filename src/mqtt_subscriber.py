from paho.mqtt import client as mqtt_client
from uuid import uuid4
from typing import NewType, Callable
import json

import sys


class MutableFlag:
    def __init__(self, value: bool):
        self.value = value


def _on_connect_default(connected, error_msg):
    if connected:
        print('mqtt subsciber connected successfully')
    else:
        print(f'failed to connect mqtt subsciber because: {error_msg}')


ConnectCallback = NewType('ConnectCallback', Callable[[bool, str], None])
# message callback is called with file name and bytes
MessageCallback = NewType('OnMessageCallback', Callable[[str, str], None])


class MqttSubscriber:
    """
    """

    def __init__(self, broker_url: str, broker_port: int, id: str = str(uuid4()), on_connect: ConnectCallback = _on_connect_default):
        self._client = self._connect_mqtt(
            broker_url, broker_port, id, on_connect)

    def subscribe(self, topic: str, on_message: MessageCallback):
        self._client.subscribe(topic)
        self._client.on_message = self._wrap_on_message(
            on_message)
        self._client.loop_forever()

    def _wrap_on_message(self, on_message):
        def _on_message(client, userdata, msg):
            payload = msg.payload.decode('utf-8')
            data = json.loads(payload)
            on_message(data['name'], data['data'])
        return _on_message

    def _connect_mqtt(self, broker_url, broker_port, id, connect):
        client = mqtt_client.Client(id)
        self._connect_blocking(client, broker_url, broker_port,
                               connect)
        return client

    def _connect_blocking(self, client, broker_url, broker_port, connect):
        connect_flag = MutableFlag(False)
        client.on_connect = self._wrap_on_connect(
            connect, connect_flag)
        client.connect(broker_url, broker_port)
        self._wait_on_callback(client, connect_flag)

    def _wrap_on_connect(self, on_connect, connect_flag):
        rc_msgs = {1: 'incorrect protocol version',
                   2: 'invalid client identifier',
                   3: 'server unavailable',
                   4: 'bad username or password',
                   5: 'not authorized'}

        def flagged_on_connect(client, userdata, flags, rc):
            connect_flag.value = True
            on_connect(rc == 0, rc_msgs.get(rc, 'unknown'))
        return flagged_on_connect

    def _wait_on_callback(self, client, connect_flag):
        client.loop_start()
        while not connect_flag.value:
            pass
        client.loop_stop()


def main(broker_url, broker_port, topic):
    subscriber = MqttSubscriber(broker_url, broker_port)

    def on_message(msg):
        print(msg)
    subscriber.subscribe(topic, on_message)


if __name__ == '__main__':
    broker_url = sys.argv[1]
    broker_port = int(sys.argv[2])
    topic = sys.argv[3]
    main(broker_url, broker_port, topic)
