from dependency_injector import providers
from pymongo import MongoClient

from .settings import settings


class MongoClientProvider(providers.Singleton):
    def __init__(self):
        super().__init__(self.create_mongo_client)

    def create_mongo_client(self):
        client = MongoClient(settings.MONGO_DSN)
        if client.ml.command('ping').get('ok'):
            return client
        raise Exception('Unable to connect to MongoDB')
