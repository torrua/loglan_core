import pytest
from loglan_core import Syllable


@pytest.mark.usefixtures("db_session")
class TestSetting:

    def test_str(self, db_session):
        syllable_1: Syllable = db_session.query(Syllable).filter(Syllable.id == 1).first()
        assert str(syllable_1) == '<BaseSyllable ID 1 vr (InitialCC)>'
