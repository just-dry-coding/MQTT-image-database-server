# quickfix includes
import sys  # noqa
from os import path  # noqa

current_directory = path.dirname(path.abspath(__file__))  # noqa
sys.path.append(current_directory)  # noqa

from mqtt_subscriber import MqttSubscriber, ConnectCallback, _on_connect_default as _on_connect_mqtt
from mongo_handler import MongoHandler, _on_connect_default as _on_connect_db

import jsonschema
import json


class ImageDataBaseServer():
    '''
        throws jsonschema.ValidationError for incorrect config
    '''

    def __init__(self, config: json):
        self.config = self._validate_input(config)

    def run(self, on_connect_db: ConnectCallback = _on_connect_db, on_connect_mqtt: ConnectCallback = _on_connect_mqtt):
        self.mongo_handler = self._create_mongo_handler(
            self.config['mongo_handler'], on_connect_db)
        self.mqtt_sub = self._create_mqtt_sub(
            self.config['mqtt_subscriber'], on_connect_mqtt)

    def _validate_input(self, config):
        current_dir = path.dirname(path.abspath(__file__))
        schema_path = path.join(current_dir, 'config_schema.json')
        with open(schema_path) as schema_file:
            schema = json.load(schema_file)
        jsonschema.validate(config, schema)
        return config

    def _create_mongo_handler(self, config, on_connect):
        return MongoHandler(config['connection_string'], config['database'], config['collection'], on_connect)

    def _create_mqtt_sub(self, config, on_connect):
        def on_message(filename, data):
            self.mongo_handler.store_image(filename, data)
        mqtt_sub = MqttSubscriber(
            config['broker_url'], config['broker_port'], on_connect=on_connect)
        mqtt_sub.subscribe(config['topic'], on_message)
        return mqtt_sub


def main(config_file):
    with open(config_file) as file:
        config = json.loads(file.read())
    image_db_server = ImageDataBaseServer(config)
    image_db_server.run()
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    config_file = sys.argv[1]
    main(config_file)
