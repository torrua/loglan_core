"""Base Model unit tests."""
import pytest

from loglan_core import Word
from loglan_core.addons.word_sourcer import WordSourcer, WordSource
from loglan_core.addons.word_selector import WordSelector
from tests.data import other_words


@pytest.mark.usefixtures("db_session")
class TestWordSources:
    """Word tests."""

    aws = WordSourcer()

    # words_objects = [Word(**obj) for obj in other_words]
    types = []
    def test_get_sources_afx(self, db_session):

        afx = Word.get_by_id(db_session, 3)
        result = self.aws.get_sources_prim(afx)
        assert result is None

    def test_get_sources_prim_c(self, db_session):

        prim_c = WordSelector().by_name("kakto").scalar(db_session)
        result = self.aws.get_sources_prim(prim_c)
        assert len(result) == 5
        assert isinstance(result, list)
        assert isinstance(result[0], WordSource)

    def test_get_sources_prim_d(self, db_session):
        db_session.add_all([Word(**w) for w in other_words])
        db_session.commit()

        prim_d = WordSelector().by_name(name="humnu").scalar(db_session)
        result = self.aws.get_sources_prim(prim_d)
        assert result == 'humnu: humni'

    def test_not_get_sources_c_prim(self, db_session):
        db_session.add_all([Word(**w) for w in other_words])
        db_session.commit()

        prim_d = WordSelector().by_name(name="humnu").scalar(db_session)
        result = self.aws._get_sources_c_prim(prim_d)
        assert result is None

    def test_get_sources_cpx(self, db_session):
        cpx = WordSelector().by_name("prukao").scalar(db_session)
        result = db_session.execute(self.aws.get_sources_cpx(cpx)).scalars().all()
        assert len(result) == 2
        assert result[0].name in ["kakto", "pruci" ]

        result = self.aws.get_sources_cpx(cpx, as_str=True)
        assert sorted(result) == sorted(['pruci', 'kakto'])

        not_cpx = WordSelector().by_name("pru").scalar(db_session)
        result = self.aws.get_sources_cpx(not_cpx)
        assert result == []

    def test_get_sources_cpd(self, db_session):
        db_session.add_all([Word(**w) for w in other_words])
        db_session.commit()
        cpd = WordSelector().by_name("aiai").scalar(db_session)
        result = db_session.execute(self.aws.get_sources_cpd(cpd)).scalars().all()
        assert len(result) == 1
        assert result[0].name == "ai"

        result = self.aws.get_sources_cpd(cpd, as_str=True)
        assert len(result) == 2
        assert result == ['ai', 'ai']

        prim = WordSelector().by_name("kakto").scalar(db_session)
        result = self.aws.get_sources_cpd(prim, as_str=True)
        assert len(result) == 0
        assert isinstance(result, list)

    def test_prepare_sources_cpx(self, db_session):
        prim = WordSelector().by_name("cii").scalar(db_session)
        assert self.aws._prepare_sources_cpx(prim) == []

    def test_prepare_sources_cpd(self, db_session):
        prim = WordSelector().by_name("cii").scalar(db_session)
        assert self.aws._prepare_sources_cpd(prim) == []

