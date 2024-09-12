import pytest

from loglan_core import WordSelector


@pytest.mark.usefixtures("db_session")
class TestBaseSelector:

    def test_without_relationships(self, db_session):
        ws = WordSelector(is_sqlite=True)
        pruci_without_relationships = ws.by_name("pruci").scalar(db_session)
        assert pruci_without_relationships is not None

        assert pruci_without_relationships.__dict__.get("definitions") is None
        assert pruci_without_relationships.__dict__.get("event_start") is None

    def test_with_relationships(self, db_session):

        kakto_with_relationships = WordSelector().by_name("kakto").with_relationships(
            selected=["definitions", "event_start"]).scalar(db_session)
        assert kakto_with_relationships.__dict__.get("definitions") is not None
        assert kakto_with_relationships.__dict__.get("event_start") is not None

        kak_with_all_relationships = WordSelector().by_name("kak").with_relationships().scalar(db_session)
        assert kak_with_all_relationships.__dict__.get("definitions") is not None
