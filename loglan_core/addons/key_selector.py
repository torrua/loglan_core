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


class KeySelector(Select):  # pylint: disable=too-many-ancestors
    """
    A class used to select keys meeting certain criteria.

    Attributes:
        class_ (Type[BaseKey]): The class to be used as the base key. It must be a subclass of BaseKey.
        is_sqlite (bool): Indicator if the object is being used with SQLite or not.
    """

    def __init__(self, class_=BaseKey, is_sqlite: bool = False) -> None:
        """
        Initializes the KeySelector object with the provided parameters.

        Args:
            class_ (Type[BaseKey]): The class to be used as the base key. Must be a subclass of BaseKey.
            is_sqlite (bool): Whether the object is being used with SQLite or not.

        Raises:
            ValueError: If the provided class_ is not a subclass of BaseKey.
        """
        if not issubclass(class_, BaseKey):
            raise ValueError(
                f"Provided attribute class_={class_} is not a {BaseKey} or its child"
            )
        super().__init__(class_)
        self.class_ = class_
        self.is_sqlite = is_sqlite

    @property
    def inherit_cache(self) -> bool:
        """
        :return: bool
        """
        return True

    def by_event(self, event_id: int | None = None) -> KeySelector:
        """
        Filters the select query by the specified Event.

        Args:
            event_id (int): The identifier of the event to filter by.

        Returns:
            A KeySelector object with the filter applied.
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

    def by_key(self, key: str, case_sensitive: bool = False) -> KeySelector:
        """
        Filters the select query by a specified key.

        Args:
            key (str): The key to filter by.
            case_sensitive (bool): Whether the key search should be case-sensitive.

        Returns:
            A KeySelector object with the filter applied.
        """
        return self.where(
            self.class_.filter_by_key_cs(key, case_sensitive, self.is_sqlite)
        )

    def by_language(self, language: str | None = None) -> KeySelector:
        """
        Filters the select query by a specified language.

        Args:
            language (str): The language to filter by.

        Returns:
            A KeySelector object with the filter applied.
        """
        return self.where(self.class_.filter_by_language(language))
