# -*- coding: utf-8 -*-
"""
This module contains an addon for basic Definition Model,
which makes it possible to get Definition objects by different criteria such as event and key.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.sql.selectable import Select

from loglan_core.connect_tables import t_connect_keys
from loglan_core.key import BaseKey
from loglan_core.word import BaseWord
from loglan_core.definition import BaseDefinition


class DefinitionSelector(Select):  # pylint: disable=too-many-ancestors
    """DefinitionSelector model"""

    def __init__(self, class_=BaseDefinition, is_sqlite: bool = False) -> None:
        """
        Initializes the object with the given parameters.

        Args:
            class_ (Type[BaseDefinition]): The class to be used as the returned object.
            Must be a subclass of BaseDefinition.
            is_sqlite (bool): Whether the object is being used with SQLite or not.

        Raises:
            ValueError: If the provided class_ is not a subclass of BaseDefinition.

        Returns:
            None
        """
        if not issubclass(class_, BaseDefinition):
            raise ValueError(
                f"Provided attribute class_={class_} is not a {BaseDefinition} or its child"
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

    def by_event(self, event_id: int | None = None) -> DefinitionSelector:
        """Select query filtered by specified Event (the latest by default)

        Args:
          event_id: int
        Returns: self object with filter applied
        """

        subquery = (
            select(self.class_.id)
            .join(t_connect_keys)
            .join(BaseWord)
            .where(BaseWord.filter_by_event_id(event_id))
            .scalar_subquery()
        )
        return self.where(self.class_.id.in_(subquery))

    def by_key(
        self,
        key: BaseKey | str,
        language: str | None = None,
        case_sensitive: bool = False,
    ) -> DefinitionSelector:
        """Definition.Query filtered by specified key

        Args:
          key: BaseKey | str:
          language: str | None:  (Default value = None)
          case_sensitive: bool:  (Default value = False)

        Returns:
          BaseQuery

        """

        search_key = key.word if isinstance(key, BaseKey) else str(key)
        filter_key = BaseKey.filter_by_key_cs(
            search_key, case_sensitive, self.is_sqlite
        )
        filter_language = BaseKey.filter_by_language(
            key.language if isinstance(key, BaseKey) else language
        )

        statement = self.join(self.class_.relationship_keys).filter(
            filter_key, filter_language
        )
        return statement.distinct()

    def by_language(self, language: str | None = None) -> DefinitionSelector:
        """Definition.Query filtered by specified language"""

        return self.filter(self.class_.filter_language(language))
