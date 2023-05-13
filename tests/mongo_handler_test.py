from unittest import TestCase

from src.mongo_handler import MongoHandler

from os import environ, path

import base64


_connection_string = environ.get('TEST_DATABASE_CONNECTION_STRING')


class MongoHandlerTest(TestCase):
    def test_connect(self):
        def test_callback(connected, _):
            assert connected

        _ = MongoHandler(_connection_string, '_', '_', test_callback)

    def test_failed_connection(self):
        def test_callback(connected, _):
            assert not connected

        mongo_handler = MongoHandler('_', '_', '_', test_callback)

        assert mongo_handler != None

    def test_store_image(self):
        mongo_handler = MongoHandler(_connection_string, 'test', 'test')

        current_dir = path.dirname(path.abspath(__file__))
        file_name = 'image1.jpg'
        absolute_path = path.join(current_dir, 'test_images', file_name)
        with open(absolute_path, 'rb') as file:
            file_data = file.read()
        success = mongo_handler.store_image(
            file_name, base64.b64encode(file_data))
        # cleanup done manually for now

        assert success
