# -*- coding: utf-8 -*-
"""Base Model unit tests."""
import pytest

from loglan_core.word import BaseWord as Word
from loglan_core.addons.word_sourcer import AddonWordSourcer

from loglan_core.word_source import BaseWordSource as WordSource


@pytest.mark.usefixtures("db_session")
class TestWord:
    """Word tests."""

    aws = AddonWordSourcer()

    def test_get_sources_afx(self, db_session):

        afx = Word.get_by_id(db_session, 3)
        result = self.aws.get_sources_prim(afx)
        assert result is None

    def test_get_sources_prim(self, db_session):

        prim = Word.get_by_id(db_session, 2)
        result = self.aws.get_sources_prim(prim)
        assert len(result) == 5
        assert isinstance(result, list)
        assert isinstance(result[0], WordSource)
