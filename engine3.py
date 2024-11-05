from typing import AsyncGenerator
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
    AsyncTransaction,
)
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

# To run async tests
pytestmark = pytest.mark.anyio

# Supply connection string
engine = create_async_engine("sqlite+aiosqlite://")


# SQLAlchemy model for demo purposes
class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str]


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


# Use this fixture to get SQLAlchemy's AsyncSession.
# All changes that occur in a test function are rolled back
# after function exits, even if session.commit() is called
# in inner functions
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


# Tests showing rollbacks between functions when using SQLAlchemy's session


async def test_create_profile(session: AsyncSession):
    existing_profiles = (await session.execute(select(Profile))).scalars().all()
    assert len(existing_profiles) == 0

    test_name = "test"
    session.add(Profile(name=test_name))
    await session.commit()

    existing_profiles = (await session.execute(select(Profile))).scalars().all()
    assert len(existing_profiles) == 1
    assert existing_profiles[0].name == test_name
