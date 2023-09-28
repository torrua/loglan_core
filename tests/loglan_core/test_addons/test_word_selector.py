import pytest
from loglan_core.addons.word_selector import (
    WordSelector,
)


@pytest.mark.usefixtures("db_session")
class TestWordGetter:
    def test_init_with_wrong_class(self, db_session):
        class TestClass:
            pass

        with pytest.raises(ValueError) as _:
            WordSelector(TestClass)

    def test_is_inherit_cache(self):
        assert WordSelector().inherit_cache is True

    def test_by_event_default_event_id(self, db_session):
        result = WordSelector().by_event()
        assert isinstance(result, WordSelector)

        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == [
            "cii",
            "flekukfoa",
            "kak",
            "kakto",
            "kao",
            "lekveo",
            "pru",
            "pruci",
            "prukao",
        ]

    def test_by_event_custom_event_id(self, db_session):
        result = WordSelector().by_event(3)
        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == [
            "kak",
            "kakto",
            "kao",
            "osmio",
            "pru",
            "pruci",
            "prukao",
            "riyhasgru",
            "riyvei",
            "testuda",
        ]

    def test_by_name_case_sensitive(self, db_session):
        name = "Pru"
        result = WordSelector(is_sqlite=True).by_name(name, case_sensitive=True)
        assert isinstance(result, WordSelector)

        result_from_db = db_session.execute(result).scalars().all()
        assert result_from_db == []

    def test_by_name_case_insensitive(self, db_session):
        name = "Pru"
        result = WordSelector(is_sqlite=True).by_name(name, case_sensitive=False)
        result_from_db = db_session.execute(result).scalars().all()
        assert len(result_from_db) == 1
        assert result_from_db[0].name == "pru"

    def test_by_name_with_wildcard(self, db_session):
        name = "pru*"
        result = WordSelector(is_sqlite=True).by_name(name)
        result_from_db = db_session.execute(result).scalars().all()
        assert len(result_from_db) == 3

    def test_by_key_with_language(self, db_session):
        key = "test"
        language = "en"
        result = WordSelector(is_sqlite=True).by_key(key=key, language=language)
        assert isinstance(result, WordSelector)

        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["pru", "pruci", "prukao"]

    def test_by_key_without_language(self, db_session):
        key = "test"
        result = WordSelector(is_sqlite=True).by_key(key=key)
        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["pru", "pruci", "prukao"]

    def test_by_key_with_foreign_language(self, db_session):
        key = "test"
        language = "es"
        result = WordSelector(is_sqlite=True).by_key(key=key, language=language)
        result_from_db = db_session.execute(result).scalars().all()
        assert len(result_from_db) == 0

    def test_by_key_case_sensitive(self, db_session):
        key = "Test"
        result = WordSelector(is_sqlite=True).by_key(key=key, case_sensitive=True)
        result_from_db = db_session.execute(result).scalars().all()
        assert len(result_from_db) == 0

    def test_by_key_case_insensitive(self, db_session):
        key = "Test"
        result = WordSelector(is_sqlite=True).by_key(key=key, case_sensitive=False)
        result_from_db = db_session.execute(result).scalars().all()
        assert len(result_from_db) == 3

    def test_by_type_with_no_parameters(self, db_session):
        result = WordSelector(is_sqlite=True).by_type()
        assert isinstance(result, WordSelector)

        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == [
            "cii",
            "flekukfoa",
            "kak",
            "kakto",
            "kao",
            "lekveo",
            "osmio",
            "pru",
            "pruci",
            "prukao",
            "riyhasgru",
            "riyvei",
            "testuda",
        ]

    def test_by_type_with_all_parameters(self, db_session):
        type_ = "2-Cpx"
        type_x = "Predicate"
        group = "Cpx"
        result = WordSelector(is_sqlite=True).by_type(
            type_=type_, type_x=type_x, group=group
        )
        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["prukao"]

    def test_by_type_with_some_parameters(self, db_session):
        type_ = "Afx"
        result = WordSelector().by_type(type_)
        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["kak", "kao", "pru"]

    def test_by_type_with_type_object(self, db_session):
        result = WordSelector().by_name("pruci")
        result_from_db = db_session.execute(result).scalars().first()
        type_ = result_from_db.type

        result = WordSelector().by_type(type_)
        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["kakto", "pruci"]

    def test_combo_by_name_and_type(self, db_session):
        result = WordSelector().by_type("Afx").by_name("ka*")
        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["kak", "kao"]
