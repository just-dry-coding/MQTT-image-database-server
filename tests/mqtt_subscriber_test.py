from unittest import TestCase

from src.mqtt_subscriber import MqttSubscriber
from .test_publisher import MqttTestPublisher

import json


BROKER_URL = 'broker.hivemq.com'
BROKER_PORT = 1883
TOPIC = 'my/super/test/unique/topic'


class MqttSubscriberTest(TestCase):
    def test_creation(self):
        mqtt_sub = MqttSubscriber(
            BROKER_URL, BROKER_PORT)

        assert mqtt_sub != None

    def test_connection(self):
        def test_callback(connected, _):
            assert connected

        _ = MqttSubscriber(
            BROKER_URL, BROKER_PORT, on_connect=test_callback)

    def test_subscription(self):
        sent_message = json.dumps({'name': 'filename',
                                   'data': 'encoded'})

        publisher = MqttTestPublisher(BROKER_URL, BROKER_PORT)

        def test_on_message(filename, data):
            sent_message_json = json.loads(sent_message)
            assert sent_message_json['name'] == filename
            assert sent_message_json['data'] == data

        mqtt_sub = MqttSubscriber(
            BROKER_URL, BROKER_PORT)

        mqtt_sub.subscribe(TOPIC, test_on_message)

        publisher.publish(TOPIC, sent_message)
