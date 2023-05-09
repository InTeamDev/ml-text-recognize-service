from dependency_injector import containers, providers

from .database import Database, Transaction
from .settings import Settings, settings


class Container(containers.DeclarativeContainer):
    db = providers.Singleton(Database, dsn=settings.get_dsn())

    transaction_provider = providers.Factory(
        Transaction,
        transaction_session=db.provided.transaction,
    )


def configure(app_settings: Settings) -> Container:
    container = Container()
    return container
