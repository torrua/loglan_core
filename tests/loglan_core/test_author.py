import pytest
from loglan_core import Author


@pytest.mark.usefixtures("db_session")
class TestAuthor:

    def test_contribution(self, db_session):
        author = db_session.query(Author).filter(Author.id == 1).first()
        assert len(author.contribution) == 4
