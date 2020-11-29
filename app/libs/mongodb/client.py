from pymongo import database, MongoClient

from configs.alpha import MONGODB_CONFIG as CONFIG


class MongoDatabase(object):
    """
    This class returns a database object, not a mongo client.
    In order to access the client, use the syntax: `database.client`
    """

    def __new__(cls, db: str = CONFIG['db'], *arg, **kwargs) -> database:
        client = MongoClient(
            host=CONFIG['host'],
            port=CONFIG['port'],
            username=CONFIG['username'],
            password=CONFIG['password'],
            authSource='admin'
        )

        return client[db]
