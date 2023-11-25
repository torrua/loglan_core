import pytest
from loglan_core import Type


@pytest.mark.usefixtures("db_session")
class TestType:

    def test_str(self, db_session):
        type_2: Type = db_session.query(Type).filter(Type.id == 2).first()
        assert str(type_2) == '<BaseType ID 2 C-Prim (Predicate)>'

    def test_words(self, db_session):
        type_2: Type = db_session.query(Type).filter(Type.id == 2).first()
        assert len(type_2.words) == 2

    def test_by(self, db_session):
        statement = Type.by_property("Predicate")
        result_from_db = db_session.execute(statement).scalars().all()
        assert len(result_from_db) == 3

        cpx: Type = db_session.query(Type).filter(Type.type == 'C-Prim').first()
        assert cpx in result_from_db
