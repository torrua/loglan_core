import pytest
from sqlalchemy import select
from loglan_core import Word, Type, Event, WordSelector, DefinitionSelector
from loglan_core.addons.base_selector import BaseSelector


@pytest.mark.usefixtures("db_session")
class TestWord:

    def test_str(self, db_session):
        kakto: Word = WordSelector().by_name("kakto").scalar(db_session)
        assert str(kakto) == "<BaseWord ID 2 kakto>"

    def test_repr(self, db_session):
        kakto: Word = WordSelector().by_name("kakto").scalar(db_session)
        assert repr(kakto) == (
            "BaseWord(event_start_id=1, id=2, id_old=3880, match='56%', name='kakto',"
            " origin='3/3R akt | 4/4S acto | 3/3F acte | 2/3E act | 2/3H kam', rank='1.0',"
            " type_id=2, year=datetime.date(1975, 1, 1))"
        )

    def test_type(self, db_session):
        prukao: Word = WordSelector().by_name("prukao").scalar(db_session)
        cpx = BaseSelector(Type).filter_by(id=prukao.type_id).scalar(db_session)
        assert prukao.type == cpx

    def test_event_start(self, db_session):
        kakto: Word = WordSelector().by_name("kakto").scalar(db_session)
        event_start: Event = (
            BaseSelector(Event).filter_by(id=kakto.event_start_id).scalar(db_session)
        )
        assert kakto.event_start == event_start

    def test_event_end(self, db_session):
        kakto: Word = WordSelector().by_name("kakto").scalar(db_session)
        event_end: Event = (
            BaseSelector(Event).filter_by(id=kakto.event_end_id).scalar(db_session)
        )
        assert kakto.event_end == event_end is None

    def test_authors(self, db_session):
        prukao: Word = WordSelector().by_name("prukao").scalar(db_session)
        assert len(prukao.authors) == 2

    def test_definitions(self, db_session):
        kakto: Word = WordSelector().by_name("kakto").scalar(db_session)
        assert len(kakto.definitions) == 5

    def test_definitions_delete_cascade(self, db_session):
        kakto: Word = WordSelector().by_name("kakto").scalar(db_session)
        kakto_definitions_count = len(kakto.definitions)
        all_definitions_count = len(DefinitionSelector().all(db_session))

        db_session.delete(kakto)
        db_session.commit()

        assert (
            len(DefinitionSelector().all(db_session))
            == all_definitions_count - kakto_definitions_count
        )

    def test_derivatives(self, db_session):
        kakto: Word = WordSelector().by_name("kakto").scalar(db_session)
        assert len(kakto.derivatives) == 3

    def test_parents(self, db_session):
        prukao: Word = WordSelector().by_name("prukao").scalar(db_session)
        kakto: Word = WordSelector().by_name("kakto").scalar(db_session)
        assert kakto in prukao.parents

    def test_affixes_hybrid_property(self, db_session):
        kakto = WordSelector().by_name("kakto").scalar(db_session)
        assert len(kakto.affixes) == 2
        assert isinstance(kakto.affixes, list)
        assert isinstance(kakto.affixes[0], Word)

    def test_complexes_hybrid_property(self, db_session):
        kakto = WordSelector().by_name("kakto").scalar(db_session)
        assert len(kakto.complexes) == 1
        assert isinstance(kakto.complexes, list)
        assert isinstance(kakto.complexes[0], Word)

    def test_affixes_hybrid_property_sql_filter(self, db_session):
        stmt = select(Word).where(Word.affixes.any())
        words_with_affixes = db_session.scalars(stmt).all()
        words_names = {w.name for w in words_with_affixes}
        assert "kakto" in words_names
        assert "pruci" in words_names

        stmt_specific = select(Word).where(Word.affixes.any(Word.name == "kak"))
        words_with_kak = db_session.scalars(stmt_specific).all()
        assert len(words_with_kak) == 1
        assert words_with_kak[0].name == "kakto"

    def test_complexes_hybrid_property_sql_filter(self, db_session):
        stmt = select(Word).where(Word.complexes.any())
        words_with_cpx = db_session.scalars(stmt).all()
        words_names = {w.name for w in words_with_cpx}
        assert "kakto" in words_names

        stmt_specific = select(Word).where(Word.complexes.any(Word.name == "prukao"))
        words_with_prukao = db_session.scalars(stmt_specific).all()
        assert len(words_with_prukao) == 2

    def test_djifoa_hybrid_property(self, db_session):
        kakto = WordSelector().by_name("kakto").scalar(db_session)
        assert kakto.djifoa == kakto.affixes
        stmt = select(Word).where(Word.djifoa.any(Word.name == "kak"))
        res = db_session.scalars(stmt).all()
        assert len(res) == 1
        assert res[0].name == "kakto"

    def test_keys(self, db_session):
        kakto: Word = WordSelector().by_name("kakto").scalar(db_session)
        assert len(kakto.keys) == 5
        assert [k.word for k in kakto.keys] == [
            "act",
            "activity",
            "actor",
            "end",
            "undertake",
        ]

    def test_word_indexes(self):
        indexed_cols = {
            col.name for idx in Word.__table__.indexes for col in idx.columns
        }
        assert "name" in indexed_cols
        assert "type" in indexed_cols
        assert "event_start" in indexed_cols
        assert "event_end" in indexed_cols

        name_idx = next(
            idx
            for idx in Word.__table__.indexes
            if Word.__table__.c.name in idx.columns.values()
        )
        assert not name_idx.unique
