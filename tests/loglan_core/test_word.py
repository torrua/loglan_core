import pytest
from loglan_core import Word, Type, Event, WordSelector
from loglan_core.addons.base_selector import BaseSelector


@pytest.mark.usefixtures("db_session")
class TestWord:

    def test_str(self, db_session):
        kakto: Word = WordSelector().by_name('kakto').scalar(db_session)
        assert str(kakto) == "<BaseWord ID 2 kakto>"

    def test_repr(self, db_session):
        kakto: Word = WordSelector().by_name('kakto').scalar(db_session)
        assert repr(kakto) == (
            "BaseWord(event_start_id=1, id=2, id_old=3880, match='56%', name='kakto',"
            " origin='3/3R akt | 4/4S acto | 3/3F acte | 2/3E act | 2/3H kam', rank='1.0',"
            " type_id=2, year=datetime.date(1975, 1, 1))"
        )

    def test_type(self, db_session):
        prukao: Word = WordSelector().by_name('prukao').scalar(db_session)
        cpx = BaseSelector(Type).filter_by(id=prukao.type_id).scalar(db_session)
        assert prukao.type == cpx

    def test_event_start(self, db_session):
        kakto: Word = WordSelector().by_name('kakto').scalar(db_session)
        event_start: Event = BaseSelector(Event).filter_by(id=kakto.event_start_id).scalar(db_session)
        assert kakto.event_start == event_start

    def test_event_end(self, db_session):
        kakto: Word = WordSelector().by_name('kakto').scalar(db_session)
        event_end: Event = BaseSelector(Event).filter_by(id=kakto.event_end_id).scalar(db_session)
        assert kakto.event_end == event_end is None

    def test_authors(self, db_session):
        prukao: Word = WordSelector().by_name('prukao').scalar(db_session)
        assert len(prukao.authors) == 2

    def test_definitions(self, db_session):
        kakto: Word = WordSelector().by_name('kakto').scalar(db_session)
        assert len(kakto.definitions) == 5

    def test_derivatives(self, db_session):
        kakto: Word = WordSelector().by_name('kakto').scalar(db_session)
        assert len(kakto.derivatives) == 3

    def test_parents(self, db_session):
        prukao: Word = WordSelector().by_name('prukao').scalar(db_session)
        kakto: Word = WordSelector().by_name('kakto').scalar(db_session)
        assert kakto in prukao.parents
        
    def test_affixes_hybrid_property(self, db_session):
        kakto = WordSelector().by_name('kakto').scalar(db_session)
        assert len(kakto.affixes) == 2
        assert isinstance(kakto.affixes, list)
        assert isinstance(kakto.affixes[0], Word)

    def test_complexes_hybrid_property(self, db_session):
        kakto = WordSelector().by_name('kakto').scalar(db_session)
        assert len(kakto.complexes) == 1
        assert isinstance(kakto.complexes, list)
        assert isinstance(kakto.complexes[0], Word)
