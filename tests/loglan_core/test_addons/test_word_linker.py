# -*- coding: utf-8 -*-
# pylint: disable=R0201, C0116, C0103, W0212
"""Base Addon Word Linker unit tests."""
'''
import pytest

from loglan_core.addons.word_linker import AddonWordLinker
from loglan_core.word import BaseWord
from loglan_core.author import BaseAuthor as Author


class Word(AddonWordLinker, BaseWord):
    """BaseWord class with Linker addon"""


@pytest.mark.usefixtures("db_session")
class TestWord:

    """Word tests."""
    def test_is_parented(self, db_session):
        parent: Word = Word.get_by_id(db_session, 2)
        child: Word = Word.get_by_id(db_session, 1)
        result = parent._is_parented(child)
        assert result is True

        parent: Word = Word.get_by_id(db_session, 3)
        result = parent._is_parented(child)
        assert result is False

    def test_add_child(self, db_session):
        cmp = Word.get_by_id(db_session, 2)
        assert cmp._parents.count() == 0

        for p in [Word.get_by_id(db_session, 4), Word.get_by_id(db_session, 5)]:
            prim = Word.get_by_id(db_session, p.id)
            result = prim.add_child(cmp)
            assert result == cmp.name

        Word.get_by_id(db_session, 4).add_child(cmp)
        assert cmp._parents.count() == 2


    def test_add_children(self, db_session):
        prim = Word.get_by_id(db_session, 1)
        assert prim.derivatives_query.count() == 0

        complexes = [Word.get_by_id(db_session, 3), Word.get_by_id(db_session, 4)]
        prim.add_children(complexes)
        assert prim.derivatives_query.count() == 2

    def test_add_author(self, db_session):
        word = Word.get_by_id(db_session, 2)
        assert len(word.authors) == 1

        author = Author.get_by_id(db_session, 1)
        word.add_author(author)
        assert len(word.authors) == 1

        author = Author.get_by_id(db_session, 2)
        word.add_author(author)
        assert len(word.authors) == 2
        assert author in word.authors


    def test_add_authors(self, db_session):

        word = Word.get_by_id(db_session, 1)
        assert len(word.authors) == 1

        local_authors = Author.get_all(db_session)
        assert len(local_authors) == 2

        word.add_authors(local_authors)
        assert len(word.authors) == 2

        assert isinstance(word.authors[0], Author)
'''