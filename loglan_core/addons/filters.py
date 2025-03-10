"""
This module provides utility functions for the loglan_core package.
"""

from sqlalchemy import select, true, func
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList
from sqlalchemy.sql.expression import ColumnElement

from ..event import BaseEvent
from ..key import BaseKey
from ..word import BaseWord


def filter_word_by_event_id(event_id: int | None) -> BooleanClauseList:
    """
    Returns a filter condition to select words associated with a specific event.

    Args:
        event_id: The id of the event to filter by. Defaults to None.

    Returns:
        BooleanClauseList: A filter condition to select words associated with a specific event.
    """
    latest_id = select(func.max(BaseEvent.event_id)).scalar_subquery()
    event_id_filter = event_id or latest_id
    start_id_condition = BaseWord.event_start_id <= event_id_filter
    end_id_condition = (
        BaseWord.event_end_id > event_id_filter
    ) | BaseWord.event_end_id.is_(None)
    return start_id_condition & end_id_condition


def filter_key_by_word_cs(
    key: str,
    case_sensitive: bool = False,
    is_sqlite: bool = False,
) -> BinaryExpression:
    """
    Returns a filter condition to select keys containing a specific word.

    Args:
        key: The word to filter by.
        case_sensitive: Whether to perform a case-sensitive search.
        is_sqlite: Whether the database is SQLite.

    Returns:
        BinaryExpression: A filter condition to select keys containing a specific word.
    """
    key = str(key).replace("*", "%")
    return (
        (BaseKey.word.op("GLOB")(key) if is_sqlite else BaseKey.word.like(key))
        if case_sensitive
        else BaseKey.word.ilike(key)
    )


def filter_key_by_language(language: str | None = None) -> ColumnElement[bool]:
    """
    Filter the language of the base key.

    Args:
        language (str or None): The language to filter by.
        If None, no language filter will be applied.

    Returns:
        ColumnElement[bool]: A filter condition for the base key's language.
    """
    return (BaseKey.language == language) if language else true()
