from unittest import TestCase

from src.mqtt_subscriber import MqttSubscriber
from .test_publisher import MqttTestPublisher


BROKER_URL = 'broker.hivemq.com'
BROKER_PORT = 1883
TOPIC = 'one/unique/nice/test/topic'


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
        sent_message = 'test_message'
        publisher = MqttTestPublisher(BROKER_URL, BROKER_PORT)

        def test_on_message(msg):
            assert msg == sent_message

        mqtt_sub = MqttSubscriber(
            BROKER_URL, BROKER_PORT)

        mqtt_sub.subscribe(TOPIC, test_on_message)

        publisher.publish(TOPIC, sent_message)
