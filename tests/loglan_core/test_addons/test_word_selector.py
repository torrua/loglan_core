import pytest

from loglan_core.addons.word_selector import WordSelector
from loglan_core.definition import BaseDefinition
from loglan_core.word import BaseWord


@pytest.mark.usefixtures("db_session")
class TestWordSelector:
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

        result_from_db = result.all(db_session)
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == [
            "kak",
            "kakto",
            "kao",
            "pru",
            "pruci",
            "prukao",
            "cii",
            "flekukfoa",
            "lekveo",
        ]

    def test_by_event_custom_event_id(self, db_session):
        result = WordSelector().by_event(3).get_statement()
        result_from_db = db_session.execute(result).scalars().all()
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == [
            "kak",
            "kakto",
            "kao",
            "pru",
            "pruci",
            "prukao",
            "osmio",
            "riyhasgru",
            "riyvei",
            "testuda",
        ]

    def test_by_name_case_sensitive(self, db_session):
        name = "Pru"
        result = WordSelector(is_sqlite=True, case_sensitive=True).by_name(name)
        assert isinstance(result, WordSelector)

        result_from_db = db_session.scalars(result.get_statement()).all()
        assert result_from_db == []

    def test_by_name_case_insensitive(self, db_session):
        result = WordSelector(is_sqlite=True, case_sensitive=False).by_name("Pru").all(db_session)
        assert len(result) == 1
        assert result[0].name == "pru"

    def test_by_name_with_wildcard(self, db_session):
        result = WordSelector(is_sqlite=True).by_name("pru*").all(db_session)
        assert len(result) == 3

    def test_by_key_with_language(self, db_session):
        key = "test"
        language = "en"
        result = WordSelector(is_sqlite=True).by_key(key=key, language=language)
        assert isinstance(result, WordSelector)

        sorted_names = [w.name for w in result.all(db_session)]
        assert sorted_names == ["pru", "pruci", "prukao"]

    def test_by_key_without_language(self, db_session):
        key = "test"
        result_from_db = WordSelector(is_sqlite=True).by_key(key=key).all(db_session)
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["pru", "pruci", "prukao"]

    def test_by_key_with_foreign_language(self, db_session):
        key = "test"
        language = "es"
        result_from_db = WordSelector(is_sqlite=True).by_key(key=key, language=language).all(db_session)
        assert len(result_from_db) == 0

    def test_by_key_case_sensitive(self, db_session):
        key = "Test"
        result_from_db = WordSelector(is_sqlite=True).by_key(key=key, case_sensitive=True).all(db_session)
        assert len(result_from_db) == 0

    def test_by_key_case_insensitive(self, db_session):
        key = "Test"
        result_from_db = WordSelector(is_sqlite=True).by_key(key=key, case_sensitive=False).all(db_session)
        assert len(result_from_db) == 3

    def test_by_type_with_no_parameters(self, db_session):
        result = WordSelector(is_sqlite=True).by_type()
        assert isinstance(result, WordSelector)

        result_from_db = result.all(db_session)
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names ==  [
            'kak', 'kakto', 'kao',
            'pru', 'pruci', 'prukao',
            'cii', 'flekukfoa', 'lekveo',
            'osmio', 'riyhasgru', 'riyvei',
            'testuda']

    def test_by_type_with_all_parameters(self, db_session):
        type_ = "2-Cpx"
        type_x = "Predicate"
        group = "Cpx"
        result_from_db = WordSelector(is_sqlite=True).by_type(
            type_=type_, type_x=type_x, group=group
        ).all(db_session)
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["prukao"]

    def test_by_type_with_some_parameters(self, db_session):
        type_ = "Afx"
        result_from_db = WordSelector().by_type(type_).all(db_session)
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["kak", "kao", "pru"]

    def test_by_type_with_type_object(self, db_session):
        result_from_db = WordSelector().by_name("pruci").scalar(db_session)
        type_ = result_from_db.type

        result_from_db = WordSelector().by_type(type_).all(db_session)
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["kakto", "pruci"]

    def test_combo_by_name_and_type(self, db_session):
        result_from_db = WordSelector().by_type("Afx").by_name("ka*").all(db_session)
        sorted_names = [w.name for w in result_from_db]
        assert sorted_names == ["kak", "kao"]


    def test_affixes(self, db_session):
        kakto = WordSelector().by_name("kakto").scalar(db_session)
        assert len(WordSelector().get_affixes_of(kakto.id).all(db_session)) == 2

    def test_complexes(self, db_session):
        kakto = WordSelector().by_name("kakto").scalar(db_session)
        assert len(WordSelector().get_complexes_of(kakto.id).all(db_session)) == 1

    def test_disable_model_check_true(self, db_session):
        result = WordSelector(model=BaseDefinition, disable_model_check=True).all(db_session)
        assert isinstance(result[0], BaseDefinition)

    def test_disable_model_check_false(self, db_session):
        with pytest.raises(ValueError) as _:
            WordSelector(model=BaseDefinition, disable_model_check=False).all(db_session)

    def test_disable_model_check_false_with_subclass(self, db_session):
        class TestWord(BaseWord):
            pass

        result = WordSelector(model=TestWord, disable_model_check=False).scalar(db_session)
        assert isinstance(result, TestWord)
