"""DefinitionSelector unit tests."""

import pytest

from loglan_core.addons.definition_selector import DefinitionSelector
from loglan_core.addons.key_selector import KeySelector
from loglan_core.definition import BaseDefinition
from loglan_core.word import BaseWord


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

    def test_disable_model_check_true(self, db_session):
        result = DefinitionSelector(model=BaseWord, disable_model_check=True).all(db_session)
        assert isinstance(result[0], BaseWord)

    def test_disable_model_check_false(self, db_session):
        with pytest.raises(ValueError) as _:
            DefinitionSelector(model=BaseWord, disable_model_check=False).all(db_session)

    def test_disable_model_check_false_with_subclass(self, db_session):
        class TestDefinition(BaseDefinition):
            pass

        result = DefinitionSelector(model=TestDefinition, disable_model_check=False).scalar(db_session)
        assert isinstance(result, TestDefinition)

    def test_by_key_raise_error(self, db_session):
        with pytest.raises(AttributeError) as _:
            DefinitionSelector(model=BaseWord, disable_model_check=True).by_key("act").scalar(db_session)

    def test_by_language_raise_error(self, db_session):
        with pytest.raises(AttributeError) as _:
            DefinitionSelector(model=BaseWord, disable_model_check=True).by_language("en").scalar(db_session)