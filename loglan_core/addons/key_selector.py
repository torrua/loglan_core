# -*- coding: utf-8 -*-
"""

This module contains an addon for basic Key Model,
which makes it possible to get Key objects by event
"""

from __future__ import annotations

from sqlalchemy import or_, select, func, and_
from sqlalchemy.sql.selectable import Select

from loglan_core.connect_tables import t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
from loglan_core.key import BaseKey
from loglan_core.word import BaseWord


class KeySelector(Select):

    def __init__(self, class_=BaseKey, is_sqlite: bool = False) -> None:
        if not issubclass(class_, BaseKey):
            raise ValueError(
                f"Provided attribute class_={class_} is not a {BaseKey} or its child"
            )
        super().__init__(class_)
        self.class_ = class_
        self.is_sqlite = is_sqlite

    @property
    def inherit_cache(self):  # pylint: disable=C0116
        return True

    def by_event(self, event_id: int | None = None) -> KeySelector:
        """Select query filtered by specified Event (the latest by default)

        Args:
          event_id: int
        Returns: self object with filter applied
        """
        max_event_id = select(
            func.max(BaseEvent.id)  # pylint: disable=E1102
        ).scalar_subquery()
        event_id_filter = event_id or max_event_id

        start_id_condition = BaseWord.event_start_id <= event_id_filter
        end_id_condition = or_(
            BaseWord.event_end_id > event_id_filter,
            BaseWord.event_end_id.is_(None),
        )
        conditions = and_(start_id_condition, end_id_condition)
        subquery = (
            select(self.class_.id)
            .join(t_connect_keys)
            .join(BaseDefinition)
            .join(BaseWord)
            .where(conditions)
            .scalar_subquery()
        )
        return self.where(self.class_.id.in_(subquery))
