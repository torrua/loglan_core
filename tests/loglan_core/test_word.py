import pytest
from loglan_core import Word, Type, Event, Key


@pytest.mark.usefixtures("db_session")
class TestWord:

    def test_str(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert str(kakto) == "<BaseWord ID 2 kakto>"

    def test_repr(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert repr(kakto) == (
            "BaseWord(event_start_id=1, id=2, id_old=3880, match='56%', "
            "name='kakto', origin='3/3R akt | 4/4S acto | 3/3F acte | 2/3E act | 2/3H kam', "
            "rank='1.0', type_id=2, year=datetime.date(1975, 1, 1))"
        )

    def test_type(self, db_session):
        prukao: Word = db_session.query(Word).filter(Word.name == 'prukao').first()
        cpx = db_session.query(Type).filter(Type.id == prukao.type_id).first()
        assert prukao.type == cpx

    def test_event_start(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        event_start: Event = db_session.query(Event).filter(Event.id == kakto.event_start_id).first()
        assert kakto.event_start == event_start

    def test_event_end(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        event_end: Event = db_session.query(Event).filter(Event.id == kakto.event_end_id).first()
        assert kakto.event_end == event_end is None

    def test_authors_query(self, db_session):
        prukao: Word = db_session.query(Word).filter(Word.name == 'prukao').first()
        assert prukao.authors_query.count() == 2

    def test_authors(self, db_session):
        prukao: Word = db_session.query(Word).filter(Word.name == 'prukao').first()
        assert len(prukao.authors) == 2

    def test_definitions_query(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert kakto.definitions_query.count() == 5

    def test_definitions(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert len(kakto.definitions) == 5

    def test_derivatives_query(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert kakto.derivatives_query.count() == 3

    def test_derivatives(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert len(kakto.derivatives) == 3

    def test_derivatives_query_by(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert kakto.derivatives_query_by(word_type_x="Affix").count() == 2

    def test_affixes(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        kao: Word = db_session.query(Word).filter(Word.name == 'kao').first()
        assert kao in kakto.affixes

    def test_complexes(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        pruci: Word = db_session.query(Word).filter(Word.name == 'pruci').first()
        assert kakto.complexes[0] == pruci.complexes[0]

    def test_parents_query(self, db_session):
        prukao: Word = db_session.query(Word).filter(Word.name == 'prukao').first()
        assert prukao.parents_query.count() == 2

    def test_parents(self, db_session):
        prukao: Word = db_session.query(Word).filter(Word.name == 'prukao').first()
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert kakto in prukao.parents

    def test_keys_query(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        keys = db_session.execute(kakto.keys_query).scalars().all()
        assert len(keys) == 6

    def test_keys(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert len(kakto.keys) == 5

        test: Key = db_session.query(Key).filter(Key.word == "act").first()
        assert test in kakto.keys
