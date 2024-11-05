import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from loglan_core.base import BaseModel as Base
from loglan_core.connect_tables import (
    t_connect_words,
    t_connect_authors,
    t_connect_keys,
)
from ..data import connect_words, connect_authors, connect_keys
from ..objects import get_objects


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


def create_db(session):
    add_objects(session)
    link_objects(session)


def link_objects(session):

    for parent_id, child_id in connect_words:
        ins = t_connect_words.insert().values(parent_id=parent_id, child_id=child_id)
        session.execute(ins)
        session.commit()

    for author_id, word_id in connect_authors:
        ins = t_connect_authors.insert().values(AID=author_id, WID=word_id)
        session.execute(ins)
        session.commit()

    for key_id, definition_id in connect_keys:
        ins = t_connect_keys.insert().values(KID=key_id, DID=definition_id)
        session.execute(ins)
        session.commit()


def add_objects(session):
    objects = get_objects()
    for obj in objects:
        session.add_all(obj)
    session.commit()
