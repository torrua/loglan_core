# -*- coding: utf-8 -*-
"""

This module contains an addon for basic Key Model,
which makes it possible to get Key objects by event
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.sql.selectable import Select

from loglan_core.connect_tables import t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.key import BaseKey
from loglan_core.word import BaseWord


class KeySelector(Select):  # pylint: disable=R0901
    """KeySelector model"""

    def __init__(self, class_=BaseKey, is_sqlite: bool = False) -> None:
        """
        Initializes the object with the given parameters.

        Args:
            class_ (Type[BaseKey]): The class to be used as the base key.
            Must be a subclass of BaseKey.
            is_sqlite (bool): Whether the object is being used with SQLite or not.

        Raises:
            ValueError: If the provided class_ is not a subclass of BaseKey.

        Returns:
            None
        """
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

        subquery = (
            select(self.class_.id)
            .join(t_connect_keys)
            .join(BaseDefinition)
            .join(BaseWord)
            .where(BaseWord.filter_by_event_id(event_id))
            .scalar_subquery()
        )
        return self.where(self.class_.id.in_(subquery))
