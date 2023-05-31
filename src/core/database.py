import motor.motor_asyncio
from dependency_injector import providers

from .settings import settings


class MongoClientProvider(providers.Singleton):
    def __init__(self):
        super().__init__(self.create_mongo_client)

    async def create_mongo_client(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DSN, serverSelectionTimeoutMS=5000)
        ping_result = await client.ml.command('ping')
        if ping_result.get('ok'):
            print('Connected to MongoDB')
            return client
        raise Exception('Unable to connect to MongoDB')
