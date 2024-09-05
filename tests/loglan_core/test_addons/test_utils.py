import pytest
from loglan_core import Word
from loglan_core.addons.utils import select_keys_query


@pytest.mark.usefixtures("db_session")
class TestUtils:

    def test_select_keys_query(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        keys = db_session.execute(select_keys_query(kakto)).scalars().all()
        assert len(keys) == 6