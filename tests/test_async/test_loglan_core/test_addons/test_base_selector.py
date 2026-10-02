import pytest
from sqlalchemy import Result

from loglan_core import WordSelector
from loglan_core.word import BaseWord


@pytest.mark.usefixtures("session")
async def test_execute(session):
    result = await WordSelector().execute_async(session)
    assert isinstance(result, Result)


@pytest.mark.usefixtures("session")
async def test_all(session):
    all_words = await WordSelector().all_async(session)
    assert len(all_words) == 13


@pytest.mark.usefixtures("session")
async def test_scalar(session):
    word = await WordSelector().scalar_async(session)
    assert isinstance(word, BaseWord)


@pytest.mark.usefixtures("session")
async def test_fetchmany(session):
    fetch_words = await WordSelector().fetchmany_async(session, size=5)
    assert len(fetch_words) == 5


@pytest.mark.usefixtures("session")
async def test_select_columns_single(session):
    result = await WordSelector().select_columns(BaseWord.name).all_async(session)
    assert len(result) == 13
    assert all(isinstance(n, str) for n in result)


@pytest.mark.usefixtures("session")
async def test_select_columns_multiple(session):
    result = (
        await WordSelector()
        .order_by(BaseWord.id)
        .select_columns(BaseWord.id, BaseWord.name)
        .all_async(session)
    )
    assert len(result) == 13
    assert len(result[0]) == 2
    assert result[0] == (1, "kak")
