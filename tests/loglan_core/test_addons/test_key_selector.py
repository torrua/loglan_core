# -*- coding: utf-8 -*-
"""KeySelector unit tests."""

import pytest

from loglan_core.addons.key_selector import KeySelector


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
        keys = db_session.execute(KeySelector().by_event(2)).scalars().all()
        result_1 = sorted(key.id for key in keys)
        assert result_1 == [2, 4, 6, 7, 8, 9, 10, 11]

    @staticmethod
    def test_by_event_unspecified(db_session):
        keys = db_session.execute(KeySelector().by_event()).scalars().all()

        result_2 = sorted(key.id for key in keys)
        assert result_2 == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
