from unittest import TestCase

from src.mongo_handler import MongoHandler

from os import environ, path


class MongoHandlerTest(TestCase):
    def test_connect(self):
        connection_string = environ.get('TEST_DATABASE_CONNECTION_STRING')

        def test_callback(connected, _):
            assert connected

        _ = MongoHandler(connection_string, '_', test_callback)

    def test_failed_connection(self):
        def test_callback(connected, _):
            assert not connected

        mongo_handler = MongoHandler('_', '_', test_callback)

        assert mongo_handler != None

    def test_store_image(self):
        connection_string = environ.get('TEST_DATABASE_CONNECTION_STRING')
        mongo_handler = MongoHandler(connection_string, 'test')

        current_dir = path.dirname(path.abspath(__file__))
        file_name = 'image1.jpg'
        absolute_path = path.join(current_dir, 'test_images', file_name)
        with open(absolute_path, 'rb') as file:
            success = mongo_handler.storeImage('test', file, file_name)
        # cleanup done manually for now

        assert success
