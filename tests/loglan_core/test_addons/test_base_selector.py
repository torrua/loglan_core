from datetime import date

import pytest
from sqlalchemy import Result

from loglan_core import WordSelector
from loglan_core.word import BaseWord


@pytest.mark.usefixtures("db_session")
class TestBaseSelector:

    def test_without_relationships(self, db_session):
        ws = WordSelector(is_sqlite=True)
        pruci_without_relationships = ws.by_name("pruci").scalar(db_session)
        assert pruci_without_relationships is not None

        assert pruci_without_relationships.__dict__.get("definitions") is None
        assert pruci_without_relationships.__dict__.get("event_start") is None

    def test_with_relationships(self, db_session):

        kakto_with_relationships = (
            WordSelector()
            .by_name("kakto")
            .with_relationships(selected=["definitions", "event_start"])
            .scalar(db_session)
        )
        assert kakto_with_relationships.__dict__.get("definitions") is not None
        assert kakto_with_relationships.__dict__.get("event_start") is not None

        kak_with_all_relationships = (
            WordSelector().by_name("kak").with_relationships().scalar(db_session)
        )
        assert kak_with_all_relationships.__dict__.get("definitions") is not None

    def test_execute(self, db_session):
        result = WordSelector().execute(db_session)
        assert isinstance(result, Result)

    def test_all(self, db_session):
        all_words = WordSelector().all(db_session)
        assert len(all_words) == 13

    def test___call__(self, db_session):
        all_words = WordSelector()
        assert len(all_words(db_session)) == 13

    def test_fetchmany(self, db_session):
        fetch_5 = WordSelector().fetchmany(db_session, 5)
        assert len(fetch_5) == 5

    def test_limit(self, db_session):
        limit_6 = WordSelector().limit(6).all(db_session)
        assert len(limit_6) == 6

    def test_offset(self, db_session):
        offset_5 = WordSelector().offset(5).all(db_session)
        assert len(offset_5) == 8

    def test_select_columns(self, db_session):
        result = WordSelector().select_columns(BaseWord.name).all(db_session)
        assert all(isinstance(item, str) for item in result)

    def test_select_columns_after_filter(self, db_session):
        result = (
            WordSelector().by_name("ka*").select_columns(BaseWord.name).all(db_session)
        )
        assert len(result) == 3
        assert all(isinstance(item, str) for item in result)

    def test_order_by(self, db_session):
        result_asc = WordSelector().order_by(BaseWord.name).all(db_session)
        result_unsorted = WordSelector().all(db_session)
        assert result_asc != result_unsorted
        assert len(result_asc) == len(result_unsorted)

    def test_filter(self, db_session):
        result = WordSelector().filter(BaseWord.name == "kakto").all(db_session)
        assert len(result) == 1
        assert result[0].name == "kakto"

    def test_where(self, db_session):
        result = (
            WordSelector()
            .where(
                BaseWord.name.in_(
                    [
                        "kakto",
                    ]
                )
            )
            .all(db_session)
        )
        assert len(result) == 1
        assert result[0].name == "kakto"

    def test_where_like_case_sensitive(self, db_session):
        result = (
            WordSelector(case_sensitive=True, is_sqlite=True)
            .where_like(name="Ka*")
            .all(db_session)
        )
        assert not result

    def test_where_like_case_insensitive(self, db_session):
        result = (
            WordSelector(case_sensitive=False, is_sqlite=True)
            .where_like(name="Ka*")
            .all(db_session)
        )
        assert len(result) == 3

    def test_where_like_int(self, db_session):
        result = (
            WordSelector(case_sensitive=False, is_sqlite=True)
            .where_like(id=1)
            .all(db_session)
        )
        assert len(result) == 1

    def test_where_like_date(self, db_session):
        result = (
            WordSelector(case_sensitive=False, is_sqlite=True)
            .where_like(year=date(1988, 1, 1))
            .all(db_session)
        )
        for r in result:
            assert r.year == date(1988, 1, 1)

        assert len(result) == 4

    def test_get_like_condition_raise_error(self, db_session):
        with pytest.raises(AttributeError) as _:
            WordSelector().get_like_condition("wrong_name", "test")

    def test_get_like_condition(self, db_session):
        # trick to get the coverage because we use sqlite but specify as False
        wrong_cond = WordSelector(
            case_sensitive=True, is_sqlite=False
        ).get_like_condition("name", "kakto")
        word = WordSelector().where(wrong_cond).scalar(db_session)
        assert word.name == "kakto"
