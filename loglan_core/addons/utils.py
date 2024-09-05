from __future__ import annotations

from sqlalchemy.sql.elements import BooleanClauseList

from loglan_core.event import BaseEvent
from loglan_core.word import BaseWord


def filter_by_event_id(event_id: int | None) -> BooleanClauseList:
    """
    Returns a filter condition to select words associated with a specific event.

    Args:
        event_id: The id of the event to filter by. Defaults to None.

    Returns:
        BooleanClauseList: A filter condition to select words associated with a specific event.
    """
    event_id_filter = event_id or BaseEvent.latest_id()
    start_id_condition = BaseWord.event_start_id <= event_id_filter
    end_id_condition = (BaseWord.event_end_id > event_id_filter) | BaseWord.event_end_id.is_(None)
    return start_id_condition & end_id_condition
