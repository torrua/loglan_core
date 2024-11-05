from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
    AsyncTransaction,
)

from loglan_core import Base
from ..objects import add_objects

DATABASE_URL = "sqlite+aiosqlite://"

engine = create_async_engine(DATABASE_URL)


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


@pytest.fixture(autouse=True)
async def async_create_db(session: AsyncSession):
    await session.run_sync(add_objects)


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
