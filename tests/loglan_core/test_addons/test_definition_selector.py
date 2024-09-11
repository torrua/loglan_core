"""DefinitionSelector unit tests."""

import pytest

from loglan_core.addons.definition_selector import DefinitionSelector
from loglan_core.addons.key_selector import KeySelector

@pytest.mark.usefixtures("db_session")
class TestDefinitionSelector:
    """DefinitionSelector tests."""

    @staticmethod
    def test_init_with_wrong_class():
        class TestClass:
            pass

        with pytest.raises(ValueError) as _:
            DefinitionSelector(TestClass)

    @staticmethod
    def test_is_inherit_cache():
        assert DefinitionSelector().inherit_cache is True

    @staticmethod
    def test_by_event_specified( db_session):
        definitions = DefinitionSelector().by_event(2).all(db_session)
        result = sorted(d.id for d in definitions)
        assert result == [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    @staticmethod
    def test_by_event_unspecified(db_session):
        definitions = DefinitionSelector().by_event().all(db_session)

        result = sorted(d.id for d in definitions)
        assert len(result) == 17

    def test_by_language(self, db_session):
        definitions = DefinitionSelector().by_language("es").all(db_session)
        assert len(definitions) == 2

    def test_by_key_as_str(self, db_session):
        definitions = DefinitionSelector().by_key("test").all(db_session)
        assert len(definitions) == 5

    def test_by_key_as_str_by_language(self, db_session):
        definitions = DefinitionSelector().by_key("test").by_language("es").all(db_session)
        assert len(definitions) == 1

    def test_by_key_as_obj_with_language(self, db_session):
        key = KeySelector().by_key("act").by_language("en").scalar(db_session)
        definitions = DefinitionSelector().by_key(key).all(db_session)
        result = sorted(d.id for d in definitions)
        assert result == [6, 9, 15, 16]

        key = KeySelector().by_key("act").by_language("es").scalar(db_session)
        definitions = DefinitionSelector().by_key(key).all(db_session)
        result = sorted(d.id for d in definitions)
        assert result == [15, ]

