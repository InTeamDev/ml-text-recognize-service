from dependency_injector import containers, providers

from backend.repositories.record_repository import RecordRepository

from .database import MongoClientProvider


class Container(containers.DeclarativeContainer):
    mongo_client = MongoClientProvider()

    record_repository = providers.Factory(RecordRepository, db_client=mongo_client)


def configure() -> Container:
    container = Container()
    return container
