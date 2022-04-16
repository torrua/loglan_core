import pytest
from loglan_core import Key


@pytest.mark.usefixtures("db_session")
class TestKey:
    def test_repr(self, db_session):
        key: Key = db_session.query(Key).filter(Key.id == 1).first()
        assert str(key) == "<BaseKey 'examine' (en)>"

    def test_definitions_query(self, db_session):

        key_act: Key = db_session.query(Key).filter(Key.word == "act").first()
        assert key_act.definitions_query.count() == 4

    def test_definitions(self, db_session):
        key_examine: Key = db_session.query(Key).filter(Key.word == "examine").first()
        assert len(key_examine.definitions) == 1

        key_act: Key = db_session.query(Key).filter(Key.word == "act").first()
        assert len(key_act.definitions) == 4
