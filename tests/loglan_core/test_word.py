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
            "BaseWord(event_start=BaseEvent(annotation='Initial', date=datetime.date(1975, 1, 1),"
            " definition='The initial vocabulary before updates.', event_id=1, id=1, name='Start', suffix='INIT'),"
            " event_start_id=1, id=2, id_old=3880, match='56%', name='kakto',"
            " origin='3/3R akt | 4/4S acto | 3/3F acte | 2/3E act | 2/3H kam', rank='1.0',"
            " type=BaseType(description='Composite Primitives, drawn from several target languages in a way that "
            "might make them recognizable in most of them. (See Loglan 1 Section 6.3.)', group='Prim', id=2, "
            "type='C-Prim', type_x='Predicate'), type_id=2, year=datetime.date(1975, 1, 1))")

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

    def test_authors(self, db_session):
        prukao: Word = db_session.query(Word).filter(Word.name == 'prukao').first()
        assert len(prukao.authors) == 2

    def test_definitions(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert len(kakto.definitions) == 5

    def test_derivatives(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert len(kakto.derivatives) == 3

    def test_parents(self, db_session):
        prukao: Word = db_session.query(Word).filter(Word.name == 'prukao').first()
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        assert kakto in prukao.parents
