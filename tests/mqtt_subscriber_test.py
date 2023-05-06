from unittest import TestCase

from src.mqtt_subscriber import MqttSubscriber

broker_url = 'broker.hivemq.com'
broker_port = 1883


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
        pass
