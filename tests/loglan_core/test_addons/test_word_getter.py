import pytest
from loglan_core.word import BaseWord
from loglan_core.addons.word_getter import AddonWordGetter


class Word(BaseWord, AddonWordGetter):
    ...


@pytest.mark.usefixtures("db_session")
class TestWord:

    def test_by_name(self, db_session):
        kakto: Word = Word.by_name(db_session, 'kakto').first()
        assert str(kakto) == "<Word ID 2 'kakto'>"

        kakto: Word = Word.by_name(session=db_session, name='kakto', event_id=1).first()
        assert str(kakto) == "<Word ID 2 'kakto'>"

    def test_by_key_default(self, db_session):
        test_words = Word.by_key(session=db_session, key="test")
        assert test_words.count() == 5

    def test_by_key_es(self, db_session):
        test_words = Word.by_key(session=db_session, key="test", language="es")
        assert test_words.count() == 0
