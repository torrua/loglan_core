import pytest
from loglan_core import Event


@pytest.mark.usefixtures("db_session")
class TestEvent:

    def test_deprecated_words(self, db_session):
        event_5: Event = db_session.query(Event).filter(Event.id == 5).first()
        assert len(event_5.deprecated_words) == 4

    def test_appeared_words(self, db_session):
        event_5: Event = db_session.query(Event).filter(Event.id == 5).first()
        assert len(event_5.appeared_words) == 3

    def test_latest(self, db_session):
        latest_event: Event = db_session.execute(Event.latest()).scalar()
        assert latest_event.id == 6
