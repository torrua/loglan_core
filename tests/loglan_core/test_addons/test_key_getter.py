# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import pytest
from loglan_core.key import BaseKey
from loglan_core.addons.key_getter import AddonKeyGetter

class Key(BaseKey, AddonKeyGetter):
    """BaseKey class with Getter addon"""


@pytest.mark.usefixtures("db_session")
class TestKey:
    """KeyGetter tests."""

    def test_by_event_specified(self, db_session):
        result_1 = sorted([key.id for key in Key.by_event(session=db_session, event_id=2).all()])
        assert result_1 == [2, 4, 6, 7, 8, 9, 10, 11]

    def test_by_event_unspecified(self, db_session):
        result_2 = sorted([key.id for key in Key.by_event(session=db_session).all()])
        assert result_2 == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
