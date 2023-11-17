# -*- coding: utf-8 -*-
"""Base Addon Word Linker unit tests."""

import pytest

from loglan_core.addons.word_linker import WordLinker
from loglan_core.word import BaseWord as Word
from loglan_core.author import BaseAuthor as Author


@pytest.mark.usefixtures("db_session")
class TestWordLinker:

    """Word tests."""
    def test_is_parented(self, db_session):
        parent: Word = Word.get_by_id(db_session, 2)
        child: Word = Word.get_by_id(db_session, 1)
        result = WordLinker._is_parented(parent, child)
        assert result is True

        parent: Word = Word.get_by_id(db_session, 3)
        result = WordLinker._is_parented(parent, child)
        assert result is False

    def test_add_child(self, db_session):
        cmp = Word.get_by_id(db_session, 2)
        assert cmp.parents_query.count() == 0

        for p in [Word.get_by_id(db_session, 4), Word.get_by_id(db_session, 5)]:
            prim = Word.get_by_id(db_session, p.id)
            result = WordLinker.add_child(prim, cmp)
            assert result == cmp.name

        parent = Word.get_by_id(db_session, 4)
        WordLinker.add_child(parent, cmp)
        assert cmp.parents_query.count() == 2

    def test_add_children(self, db_session):
        prim = Word.get_by_id(db_session, 1)
        assert prim.derivatives_query.count() == 0

        complexes = [Word.get_by_id(db_session, 3), Word.get_by_id(db_session, 4)]
        WordLinker.add_children(prim, complexes)
        assert prim.derivatives_query.count() == 2

        # adding already existed children
        complexes = [Word.get_by_id(db_session, 3), Word.get_by_id(db_session, 4)]
        WordLinker.add_children(prim, complexes)
        assert prim.derivatives_query.count() == 2

    def test_add_author(self, db_session):
        word = Word.get_by_id(db_session, 2)
        assert len(word.authors) == 1

        author = Author.get_by_id(db_session, 1)
        WordLinker.add_author(word, author)
        assert len(word.authors) == 1

        author = Author.get_by_id(db_session, 2)
        WordLinker.add_author(word, author)
        assert len(word.authors) == 2
        assert author in word.authors


    def test_add_authors(self, db_session):

        word = Word.get_by_id(db_session, 1)
        assert len(word.authors) == 1

        local_authors = Author.get_all(db_session)
        assert len(local_authors) == 2

        WordLinker.add_authors(word, local_authors)
        assert len(word.authors) == 2
        assert isinstance(word.authors[0], Author)

        # adding already existed authors
        WordLinker.add_authors(word, local_authors)
        assert len(word.authors) == 2
        assert isinstance(word.authors[0], Author)
