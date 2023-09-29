# -*- coding: utf-8 -*-
"""
This module contains a special class WordSelector for
extracting words from db by criteria or combinations thereof:
    event, key, type, name
"""
from __future__ import annotations

from functools import wraps

from sqlalchemy import or_, and_, func, select, true
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.selectable import Select

from loglan_core.connect_tables import t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
from loglan_core.key import BaseKey
from loglan_core.type import BaseType
from loglan_core.word import BaseWord


def order_by_name(function):
    """
    :param function:
    :return:
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
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
        max_event_id = select(
            func.max(BaseEvent.id)  # pylint: disable=E1102
        ).scalar_subquery()
        event_id_filter = event_id or max_event_id

        start_id_condition = self.class_.event_start_id <= event_id_filter
        end_id_condition = or_(
            self.class_.event_end_id > event_id_filter,
            self.class_.event_end_id.is_(None),
        )
        conditions = and_(start_id_condition, end_id_condition)
        query = self.where(conditions)
        return query

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
        name = str(name).replace("*", "%")
        conditions = (
            self.cs_name_filter(name)
            if case_sensitive
            else self.class_.name.ilike(name)
        )
        query = self.where(conditions)
        return query

    def cs_name_filter(self, name: str) -> BinaryExpression:
        """case sensitive name filter"""
        return (
            self.class_.name.op("GLOB")(name)
            if self.is_sqlite
            else self.class_.name.like(name)
        )

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

        key = key.word if isinstance(key, BaseKey) else str(key).replace("*", "%")
        key_filter = self.cs_key_filter(key, case_sensitive)
        language_filter = BaseKey.language == language if language else true()

        subquery = (
            select(self.class_.id)
            .join(BaseDefinition)
            .join(t_connect_keys)
            .join(BaseKey)
            .where(key_filter, language_filter)
            .scalar_subquery()
        )
        query = self.where(self.class_.id.in_(subquery))
        return query

    def cs_key_filter(self, key: str, case_sensitive: bool) -> BinaryExpression:
        """case sensitive name filter"""
        return (
            (BaseKey.word.op("GLOB")(key) if self.is_sqlite else BaseKey.word.like(key))
            if case_sensitive
            else BaseKey.word.ilike(key)
        )

    @order_by_name
    def by_type(
        self,
        type_: BaseType | str | None = None,
        type_x: str | None = None,
        group: str | None = None,
    ) -> WordSelector:
        """Select query filtered by specified type

        Args:
          type_: BaseType | str | None
          type_x: str | None
          group: str | None
        Returns: self object with filter applied
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
