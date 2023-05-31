import motor.motor_asyncio

from core.settings import settings


class BaseRepository:
    def __init__(self):
        db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DSN, serverSelectionTimeoutMS=5000)
        self.db = db_client.ml

    async def is_lock(self, video_id: str) -> bool:
        return await self.db.queue.find_one({"type": "lock", "video_id": video_id}) is not None

    async def lock(self, video_id: str):
        return await self.db.queue.insert_one({"type": "lock", "video_id": video_id})

    async def unlock(self, video_id: str):
        return await self.db.queue.delete_one({"type": "lock", "video_id": video_id})
