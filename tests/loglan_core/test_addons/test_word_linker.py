"""Base Addon Word Linker unit tests."""

import pytest

from sqlalchemy import select, delete
from loglan_core.addons.word_linker import WordLinker
from loglan_core.word import BaseWord as Word
from loglan_core.author import BaseAuthor as Author
from loglan_core.connect_tables import t_connect_words

@pytest.mark.usefixtures("db_session")
class TestWordLinker:

    @staticmethod
    def get_word_by_name(name: str, session):
        return session.execute(select(Word).where(Word.name==name)).scalars().first()

    @staticmethod
    def delete_links(db_session):
        delete_query = delete(t_connect_words)
        db_session.execute(delete_query)

    def test_removed_links(self, db_session):
        self.delete_links(db_session)
        cmp = self.get_word_by_name(name="prukao", session=db_session)
        assert len(cmp.parents) == 0

    def test_add_child_correct(self, db_session):
        self.delete_links(db_session)
        prukao = self.get_word_by_name(name="prukao", session=db_session)
        kakto = self.get_word_by_name(name="kakto", session=db_session)
        pruci = self.get_word_by_name(name="pruci", session=db_session)

        WordLinker.add_child(kakto, prukao)
        assert len(prukao.parents) == 1

        WordLinker.add_child(pruci, prukao)
        assert len(prukao.parents) == 2

        # adding already existed child
        WordLinker.add_child(pruci, prukao)
        assert len(prukao.parents) == 2


    def test_add_child_exception(self, db_session):
        kakto = self.get_word_by_name(name="kakto", session=db_session)
        pruci = self.get_word_by_name(name="pruci", session=db_session)
        with pytest.raises(TypeError):
            WordLinker.add_child(kakto, pruci)

    def test_add_children_correct(self, db_session):
        self.delete_links(db_session)

        kakto = self.get_word_by_name(name="kakto", session=db_session)
        kak = self.get_word_by_name(name="kak", session=db_session)
        kao = self.get_word_by_name(name="kao", session=db_session)

        assert len(kak.parents) == 0
        assert len(kao.parents) == 0

        WordLinker.add_children(kakto, [kak, kao])
        assert len(kak.parents) == 1
        assert len(kao.parents) == 1

        # adding already existed children
        WordLinker.add_children(kakto, [kak, kao])
        assert len(kak.parents) == 1
        assert len(kao.parents) == 1


    def test_add_children_exception(self, db_session):
        pruci = self.get_word_by_name(name="pruci", session=db_session)
        pru = self.get_word_by_name(name="pru", session=db_session)

        with pytest.raises(TypeError):
            WordLinker.add_children(pru, [pruci, ])

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
