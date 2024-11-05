import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from loglan_core.base import BaseModel as Base
from ..objects import create_db


@pytest.fixture(scope="function")
def db_engine():
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_engine("sqlite://", echo=False)
    Base.metadata.create_all(engine_)
    yield engine_
    Base.metadata.drop_all(engine_)
    engine_.dispose()


@pytest.fixture(scope="function")
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine, future=True))


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_: Session = db_session_factory()
    create_db(session_)

    yield session_

    session_.rollback()
    session_.close()
