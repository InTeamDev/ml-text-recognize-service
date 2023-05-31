import motor.motor_asyncio

from core.settings import settings

from .base_repository import BaseRepository


class RecordRepository(BaseRepository):
    def __init__(self):
        db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DSN, serverSelectionTimeoutMS=5000)
        self.db = db_client.ml
        self.collection = self.db["records"]

    async def create(self, record: dict) -> str:
        return await self.collection.insert_one(record).inserted_id

    async def get(self, record_id: str) -> dict:
        return await self.collection.find_one({"_id": record_id}).__dict__

    async def findByVideoInfoUrl(self, url: str):
        return await self.collection.find_one({"video_info.url": url})

    async def findByVideoInfoId(self, video_info_id: str):
        return await self.collection.find_one({"video_info.id": video_info_id})
