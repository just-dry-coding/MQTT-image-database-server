from pymongo import MongoClient
from pymongo.errors import PyMongoError

from gridfs import GridFS

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

    def __init__(self, connection_string, database, on_connect=_on_connect_default):
        self.client = MongoClient(connection_string)
        self._check_connection(on_connect)
        self.database = self.client[database]

    def storeImage(self, collection, image, file_name) -> bool:
        fs = GridFS(self.database, collection=collection)
        file_id = fs.put(image, filename=file_name)
        if fs.exists(file_id):
            return True
        return False

    def _check_connection(self, on_connect):
        try:
            _ = self.client.server_info()
            on_connect(True, '')
        except PyMongoError as e:
            on_connect(False, str(e))
