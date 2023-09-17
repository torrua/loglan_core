import pytest
from loglan_core import Author
from sqlalchemy import select

@pytest.mark.usefixtures("db_session")
class TestAuthor:
    def test_contribution(self, db_session):
        stmt = select(Author).where(Author.id == 1)
        author = db_session.execute(stmt).scalar()
        assert len(author.contribution) == 4