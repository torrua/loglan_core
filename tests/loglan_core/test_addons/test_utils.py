import pytest

from loglan_core import Word, Type
from loglan_core.addons.utils import select_keys_query, select_type_by_property


@pytest.mark.usefixtures("db_session")
class TestUtils:

    def test_select_keys_query(self, db_session):
        kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
        keys = db_session.execute(select_keys_query(kakto)).scalars().all()
        assert len(keys) == 6


    def test_by(self, db_session):
        statement = select_type_by_property("Predicate")
        result_from_db = db_session.execute(statement).scalars().all()
        assert len(result_from_db) == 3

        cpx: Type = db_session.query(Type).filter(Type.type == 'C-Prim').first()
        assert cpx in result_from_db
