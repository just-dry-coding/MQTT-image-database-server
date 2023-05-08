from unittest import TestCase
from pytest import raises

from src.image_database_server import ImageDataBaseServer
import json
from jsonschema import ValidationError

from os import environ

connection_string = environ.get('TEST_DATABASE_CONNECTION_STRING')

config = '{ \
            "mqtt_subscriber":{ \
                "broker_url": "broker.hivemq.com", \
                "broker_port": 1883, \
                "topic": "one/unique/nice/test/topic" \
            }, \
            "mongo_handler":{ \
                "connection_string": "", \
                "database": "test", \
                "collection": "test" \
            } \
        }'


class ImageDatabaseServerTest(TestCase):
    def test_validation(self):
        try:
            _ = ImageDataBaseServer(json.loads(config))
            assert True
        except ValidationError:
            assert False

    def test_run(self):
        json_config = json.loads(config)
        json_config['mongo_handler']['connection_string'] = connection_string
        img_database_server = ImageDataBaseServer(json_config)

        def test_callback_db(connected, _):
            assert connected

        def test_callback_mqtt(connected, _):
            assert connected

        img_database_server.run(test_callback_db, test_callback_mqtt)
