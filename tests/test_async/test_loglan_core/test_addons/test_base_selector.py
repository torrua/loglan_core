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
