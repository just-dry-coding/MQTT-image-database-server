from unittest import TestCase

from src.mqtt_subscriber import MqttSubscriber
from .test_publisher import MqttTestPublisher


broker_url = 'broker.hivemq.com'
broker_port = 1883
topic = 'one/unique/nice/test/topic'


class MqttSubscriberTest(TestCase):
    def test_creation(self):
        mqtt_sub = MqttSubscriber(
            broker_url, broker_port)

        assert mqtt_sub != None

    def test_connection(self):
        def test_callback(rc):
            assert rc == 0

        mqtt_sub = MqttSubscriber(
            broker_url, broker_port, on_connect=test_callback)

    def test_subscription(self):
        sent_message = 'test_message'
        publisher = MqttTestPublisher(broker_url, broker_port)

        def test_on_message(msg):
            assert msg == sent_message

        mqtt_sub = MqttSubscriber(
            broker_url, broker_port)

        mqtt_sub.subscribe(topic, test_on_message)

        publisher.publish(topic, sent_message)
