from typing import AsyncGenerator

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
    AsyncTransaction,
)

from loglan_core.connect_tables import (
    t_connect_words,
    t_connect_authors,
    t_connect_keys,
)

from tests.data import connect_words, connect_authors, connect_keys, Base, Word
from tests.objects import get_objects

DATABASE_URL = "sqlite+aiosqlite://"

engine = create_async_engine(DATABASE_URL)


async def async_link_objects(session: AsyncSession):
    for parent_id, child_id in connect_words:
        ins = t_connect_words.insert().values(parent_id=parent_id, child_id=child_id)
        await session.execute(ins)
    await session.commit()

    for author_id, word_id in connect_authors:
        ins = t_connect_authors.insert().values(AID=author_id, WID=word_id)
        await session.execute(ins)
    await session.commit()

    for key_id, definition_id in connect_keys:
        ins = t_connect_keys.insert().values(KID=key_id, DID=definition_id)
        await session.execute(ins)
    await session.commit()


async def async_add_objects(session: AsyncSession):
    objects = get_objects()  # Ensure this returns a list of objects
    for obj in objects:
        session.add_all(obj)  # Add all objects at once
        await session.commit()


@pytest.fixture(autouse=True)
async def async_create_db(session: AsyncSession):
    await async_add_objects(session)
    await async_link_objects(session)


# To run async tests
pytestmark = pytest.mark.anyio


# Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def connection(anyio_backend) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection


@pytest.fixture(scope="session", autouse=True)
async def setup_database(connection: AsyncConnection):
    # Create the tables in the database
    async with connection.begin():
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction


@pytest.fixture()
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )
    yield async_session

    await transaction.rollback()


async def test_add_profiles(session: AsyncSession):
    existing_profiles = await session.execute(select(Word))
    existing_profiles = existing_profiles.scalars().all()
    assert len(existing_profiles) == 13
