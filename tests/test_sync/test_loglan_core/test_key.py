import pytest
from loglan_core import Key


@pytest.mark.usefixtures("db_session")
class TestKey:
    def test_str(self, db_session):
        key: Key = db_session.query(Key).filter(Key.id == 1).first()
        assert str(key) == "<BaseKey 1 'examine' (en)>"

    def test_definitions(self, db_session):
        key_examine: Key = db_session.query(Key).filter(Key.word == "examine").first()
        assert len(key_examine.definitions) == 1

        key_act: Key = db_session.query(Key).filter(Key.word == "act").first()
        assert len(key_act.definitions) == 4
