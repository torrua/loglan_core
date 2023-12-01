import pytest
from loglan_core import Definition, Key, Word


@pytest.mark.usefixtures("db_session")
class TestDefinition:

    def test_str(self, db_session):
        definition: Definition = db_session.query(Definition).filter_by(id=1).first()
        assert str(definition) == '<BaseDefinition ID 1/6 K «test»/«examine» B…>'

    def test_keys_query(self, db_session):
        definition: Definition = db_session.query(Definition).filter_by(id=1).first()
        assert definition.keys_query.count() == 2

    def test_keys(self, db_session):
        definition: Definition = db_session.query(Definition).filter_by(id=1).first()
        assert len(definition.keys) == 2

        test: Key = db_session.query(Key).filter(Key.word == "test").first()
        assert test in definition.keys

    def test_source_word(self, db_session):
        definition: Definition = db_session.query(Definition).filter_by(id=1).first()
        prukao: Word = db_session.query(Word).filter(Word.name == 'prukao').first()
        assert definition.source_word == prukao

    def test_grammar(self, db_session):
        definition: Definition = db_session.query(Definition).filter_by(id=1).first()
        assert definition.grammar == "(4v)"
