import pytest
from loglan_core import Type


@pytest.mark.usefixtures("db_session")
class TestType:

    def test_words(self, db_session):
        type_2: Type = db_session.query(Type).filter(Type.id == 2).first()
        assert len(type_2.words) == 2

    def test_by(self, db_session):
        types = Type.by(db_session, "Predicate")
        assert len(types) == 2

        cpx: Type = db_session.query(Type).filter(Type.type == 'C-Prim').first()
        assert cpx in types

