from pymongo import MongoClient
from pymongo.errors import PyMongoError

from gridfs import GridFS
import base64

from os import path
import sys

from typing import NewType, Callable


def _on_connect_default(connected, error_msg):
    if connected:
        print('mongo handler connected successfully')
    else:
        print(f'failed to connect mongo handler because: {error_msg}')


ConnectCallback = NewType('ConnectCallback', Callable[[bool, str], None])


class MongoHandler():
    """
        todo: docu write interface and methods
    """

    def __init__(self, connection_string: str, database: str, collection: str, on_connect: ConnectCallback = _on_connect_default):
        self.client = MongoClient(connection_string)
        self._check_connection(on_connect)
        self.database = self.client[database]
        self.fs = GridFS(self.database, collection=collection)

    def store_image(self,  file_name: str, image_data: str) -> bool:
        decoded_data = base64.b64decode(image_data)
        file_id = self.fs.put(decoded_data, filename=file_name)
        if self.fs.exists(file_id):
            return True
        return False

    def _check_connection(self, on_connect):
        try:
            _ = self.client.server_info()
            on_connect(True, '')
        except PyMongoError as e:
            on_connect(False, str(e))


def main(connection_string, database, collection, img_path, img_name):
    mongo_handler = MongoHandler(connection_string, database)
    complete_path = path.join(img_path, img_name)
    with open(complete_path, 'rb') as file:
        success = mongo_handler.store_image(collection, file, img_name)
    print("success" if success else "failed")


if __name__ == '__main__':
    connection_string = sys.argv[1]
    database = sys.argv[2]
    collection = sys.argv[3]
    img_path = sys.argv[4]
    img_name = sys.argv[5]
    main(connection_string, database, collection, img_path, img_name)
