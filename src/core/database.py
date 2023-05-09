from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker

Base = declarative_base()


class Database:
    def __init__(self, dsn: str) -> None:
        self._engine = create_engine(dsn)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @contextmanager
    def transaction(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            self._session_factory.remove()


class Transaction:
    def __init__(self, transaction_session: Callable[..., AbstractContextManager[Session]]):
        self.transaction = transaction_session
