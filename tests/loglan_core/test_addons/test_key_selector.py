"""KeySelector unit tests."""

import pytest

from loglan_core.addons.key_selector import KeySelector
from loglan_core.addons.word_selector import WordSelector


@pytest.mark.usefixtures("db_session")
class TestKeySelector:
    """KeySelector tests."""

    @staticmethod
    def test_init_with_wrong_class():
        class TestClass:
            pass

        with pytest.raises(ValueError) as _:
            KeySelector(TestClass)

    @staticmethod
    def test_is_inherit_cache():
        assert KeySelector().inherit_cache is True

    @staticmethod
    def test_by_event_specified( db_session):
        keys = KeySelector().by_event(2).all(db_session)
        result = sorted(key.id for key in keys)
        assert result == [2, 4, 6, 7, 8, 9, 10, 11, 12]

    @staticmethod
    def test_by_event_unspecified(db_session):
        keys = KeySelector().by_event().all(db_session)

        result = sorted(key.id for key in keys)
        assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    @staticmethod
    def test_by_key(db_session):
        keys = KeySelector().by_key("act").all(db_session)

        result = sorted(key.id for key in keys)
        assert result == [7, 12]

    @staticmethod
    def test_by_language(db_session):
        keys = KeySelector().by_language("es").all(db_session)

        result = sorted(key.id for key in keys)
        assert result == [12, 14]

    @staticmethod
    def test_by_key_and_language(db_session):
        keys = KeySelector(is_sqlite=True, ).by_language("es").by_key("act").all(db_session)

        result = sorted(key.id for key in keys)
        assert result == [12, ]

    @staticmethod
    def test_by_key_cs(db_session):
        keys = KeySelector(is_sqlite=True, case_sensitive=True).by_key("Act").all(db_session)
        assert keys == []

    @staticmethod
    def test_by_key_wildcard(db_session):
        keys = KeySelector(is_sqlite=True).by_key("Act*").all(db_session)

        result = sorted(key.id for key in keys)
        assert result == [7, 9, 11, 12, ]

    @staticmethod
    def test_by_word_id(db_session):
        kakto = WordSelector(is_sqlite=True).by_name("kakto").scalar(db_session)
        keys = KeySelector(is_sqlite=True).by_word_id(kakto.id).all(db_session)
        assert len(keys) == 5
