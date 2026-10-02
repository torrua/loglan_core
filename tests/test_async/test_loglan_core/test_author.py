import pytest
from sqlalchemy import select
from loglan_core import Author, Word


@pytest.mark.usefixtures("session")
class TestAsyncAuthor:
    async def test_str(self, session):
        stmt = select(Author).filter(Author.id == 1)
        author = (await session.scalars(stmt)).first()
        assert author is not None
        assert str(author) == "<BaseAuthor ID 1 L4>"

    async def test_contribution_relationship(self, session):
        stmt = select(Author).filter(Author.id == 1)
        author = (await session.scalars(stmt)).first()
        assert author is not None
        contribution = await author.awaitable_attrs.contribution
        assert len(contribution) == 4
        assert isinstance(contribution[0], Word)
