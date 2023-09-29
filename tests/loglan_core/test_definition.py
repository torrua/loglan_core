import pytest
from loglan_core import Definition, Key, Word


@pytest.mark.usefixtures("db_session")
class TestDefinition:

    def test_repr(self, db_session):
        definition: Definition = db_session.query(Definition).filter_by(id=1).first()
        assert str(definition) == '<BaseDefinition ID 1/6 - K «test»/«examine» B...>'

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

    def test_by_key(self, db_session):
        definitions_test_en = Definition.by_key("test", "en")
        result = db_session.execute(definitions_test_en).scalars().all()
        assert len(result) == 5

        definitions_act = Definition.by_key("act")
        result = db_session.execute(definitions_act).scalars().all()
        assert len(result) == 4
