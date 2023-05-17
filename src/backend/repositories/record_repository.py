from pymongo.collection import Collection


class RecordRepository:
    def __init__(self, db_client):
        self.db = db_client.ml
        self.collection: Collection = self.db.records

    def create(self, record: dict) -> str:
        return self.collection.insert_one(record).inserted_id

    def get(self, record_id: str) -> dict:
        return self.collection.find_one({"_id": record_id}).__dict__

    def findByVideoInfoUrl(self, url: str):
        return self.collection.find_one({"video_info.url": url})

    def findByVideoInfoId(self, video_info_id: str):
        return self.collection.find_one({"video_info.id": video_info_id})
