# -*- coding: utf-8 -*-
"""
This module contains a special class WordSelector for
extracting words from db by criteria or combinations thereof:
    event, key, type, name
"""
from __future__ import annotations

from functools import wraps

from sqlalchemy import and_, select
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.selectable import Select

from loglan_core.definition import BaseDefinition
from loglan_core.key import BaseKey
from loglan_core.type import BaseType
from loglan_core.word import BaseWord


def order_by_name(function):
    """
    Decorator that sorts the result of a function by the `name` attribute of its class.

    Args:
        function: The function to be decorated.

    Returns:
        The decorated function that applies the sorting logic.

    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        """
        Wrapper function that applies the sorting logic to the result of the decorated function.

        Args:
            *args: Positional arguments to be passed to the decorated function.
            **kwargs: Keyword arguments to be passed to the decorated function.

        Returns:
            The sorted result of the decorated function.

        """
        result = function(*args, **kwargs)
        return result.order_by(result.class_.name)

    return wrapper


class WordSelector(Select):  # pylint: disable=R0901
    """WordSelector model"""

    def __init__(self, class_=BaseWord, is_sqlite: bool = False) -> None:
        if not issubclass(class_, BaseWord):
            raise ValueError(
                f"Provided attribute class_={class_} is not a {BaseWord} or its child"
            )
        super().__init__(class_)
        self.class_ = class_
        self.is_sqlite = is_sqlite

    @property
    def inherit_cache(self):  # pylint: disable=C0116
        return True

    @order_by_name
    def by_event(self, event_id: int | None = None) -> WordSelector:
        """Select query filtered by specified Event (the latest by default)

        Args:
          event_id: int
        Returns: self object with filter applied
        """
        return self.where(self.class_.filter_by_event_id(event_id))

    @order_by_name
    def by_name(
        self,
        name: str,
        case_sensitive: bool = False,
    ) -> WordSelector:
        """Select query filtered by specified name

        Args:
          name: str:
          case_sensitive: bool:  (Default value = False)
        Returns: self object with filter applied
        """
        statement = self.class_.filter_by_name_cs(
            name=name,
            case_sensitive=case_sensitive,
            is_sqlite=self.is_sqlite,
        )
        query = self.where(statement)
        return query

    @order_by_name
    def by_key(
        self,
        key: BaseKey | str,
        language: str | None = None,
        case_sensitive: bool = False,
    ) -> WordSelector:
        """Select query filtered by specified key

        Args:
          key: Union[BaseKey, str]
          language: str: Language of key (Default value = None)
          case_sensitive: bool:  (Default value = False)
        Returns: self object with filter applied
        """

        definition_query = BaseDefinition.by_key(
            key=key,
            language=language,
            case_sensitive=case_sensitive,
            is_sqlite=self.is_sqlite,
        )
        subquery = select(definition_query.subquery().c.word_id)
        query = self.where(self.class_.id.in_(subquery))
        return query

    @order_by_name
    def by_type(
        self,
        type_: BaseType | str | None = None,
        type_x: str | None = None,
        group: str | None = None,
    ) -> WordSelector:
        """
        Select query filtered by specified type

        Args:
          type_: BaseType | str | None
          type_x: str | None
          group: str | None
        Returns:
            self object with filter applied
        """

        if isinstance(type_, BaseType):
            return self.join(BaseType).where(BaseType.id == type_.id)

        type_values: tuple[tuple[InstrumentedAttribute, str | None | BaseType], ...] = (
            (BaseType.type, type_),
            (BaseType.type_x, type_x),
            (BaseType.group, group),
        )

        type_filters = self.type_filters(type_values)

        return (
            self if not type_filters else self.join(BaseType).where(and_(*type_filters))
        )

    @staticmethod
    def type_filters(type_values: tuple) -> list[BinaryExpression]:
        """collection of type filters"""
        type_filters = [
            i[0].ilike(str(i[1]).replace("*", "%")) for i in type_values if i[1]
        ]
        return type_filters
