from __future__ import annotations

from sqlalchemy import select, Select, true
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.expression import ColumnElement

from loglan_core import t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
from loglan_core.key import BaseKey
from loglan_core.word import BaseWord


def filter_word_by_event_id(event_id: int | None) -> BooleanClauseList:
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


def filter_key_by_word_cs(
    key: str,
    case_sensitive: bool = False,
    is_sqlite: bool = False,
) -> BinaryExpression:
    """case sensitive name filter"""
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


def select_keys_query(word: BaseWord) -> Select:
        """Get all BaseKey object related to BaseWord.

        Keep in mind that duplicated keys from related definitions
        will be counted with ```.count()``` but excluded from ```.all()``` request

        Returns:
        """
        return (
            select(BaseKey)
            .join(t_connect_keys)
            .join(BaseDefinition, BaseDefinition.id == t_connect_keys.c.DID)
            .join(BaseWord, BaseWord.id == BaseDefinition.word_id)
            .filter(BaseWord.id == word.id)
            .order_by(BaseKey.word.asc())
        )
