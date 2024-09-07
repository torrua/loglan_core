import pytest

from loglan_core.addons.base_selector import BaseSelector
from loglan_core import Word, WordSelector


@pytest.mark.usefixtures("db_session")
class TestBaseSelector:
    def test_condition_by_attribute_with_wrong_class(self, db_session):
        class TestClass:
            pass

        with pytest.raises(ValueError) as _:
            BaseSelector.condition_by_attribute(TestClass, "test", "test")

    def test_condition_by_attribute_wrong_attr(self, db_session):
        with pytest.raises(AttributeError) as _:
            BaseSelector.condition_by_attribute(Word, "test", "test")

    def test_condition_by_attribute_no_use_wildcard(self, db_session):
        result = BaseSelector.condition_by_attribute(Word, "name", "kakt*", use_wildcard=False)
        result_from_db = WordSelector(is_sqlite=True).where(result).all(db_session)
        assert not len(result_from_db)