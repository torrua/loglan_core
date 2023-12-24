"""
This module provides a mechanism to extract words
from a database based on various criteria such as
event, key, type, and name through the WordSelector class.
"""

from __future__ import annotations

from functools import wraps
from typing import Type

from sqlalchemy import and_, select
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression

from loglan_core.addons.base_selector import BaseSelector
from loglan_core.addons.definition_selector import DefinitionSelector
from loglan_core.key import BaseKey
from loglan_core.type import BaseType
from loglan_core.word import BaseWord


def order_by_name(function):
    """
    A decorator that sorts the output of a function by the `name` attribute of
    the resulting class instances.

    Args:
        function (callable): The function whose result is to be sorted.

    Returns:
        callable: A function that will execute the input function and sort its result.
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


class WordSelector(BaseSelector):  # pylint: disable=R0901
    """
    Class to extract words from a database based on various criteria.

    Extends the SQLAlchemy Select class to provide additional functionality.
    """

    def __init__(self, class_: Type[BaseWord] = BaseWord, is_sqlite: bool = False):
        """
        Initialize a WordSelector instance.

        Args:
            class_ (BaseWord): The class to select from. Defaults to BaseWord.
            is_sqlite (bool): If SQLite is being used. Defaults to False.
        """
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
        """
        Applies a filter to select words associated with a specific event.

        Args:
            event_id (int | None): The id of the event to filter by. Defaults to None.

        Returns:
            WordSelector: A query with the filter applied.
        """
        return self.where(self.class_.filter_by_event_id(event_id))

    @order_by_name
    def by_name(
        self,
        name: str,
        case_sensitive: bool = False,
    ) -> WordSelector:
        """
        Applies a filter to select words by a specific name.

        Args:
            name (str): The name to filter by.
            case_sensitive (bool): Whether the search should be case-sensitive.
            Defaults to False.

        Returns:
            WordSelector: A query with the filter applied.
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
        """
        Applies a filter to select words by a specific key.

        Args:
            key (BaseKey | str): The key to filter by.
            It can either be an instance of BaseKey or a string.
            language (str | None): The language of the key. Defaults to None.
            case_sensitive (bool): Whether the search should be case-sensitive.
                Defaults to False.

        Returns:
            WordSelector: A query with the filter applied.
        """

        definition_query = DefinitionSelector(is_sqlite=self.is_sqlite).by_key(
            key=key,
            language=language,
            case_sensitive=case_sensitive,
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
        Applies a filter to select words by a specific type.

        Args:
            type_ (BaseType | str | None): The type to filter by.
            It can either be an instance of BaseType, a string, or None.
            type_x (str | None): The extended type to filter by. Defaults to None.
            group (str | None): The group to filter by. Defaults to None.

        Returns:
            WordSelector: A query with the filter applied.
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
        """
        Builds a collection of type filters based on provided type values.

        Args:
            type_values (tuple): A tuple containing values for type, type_x, and group.

        Returns:
            list[BinaryExpression]: A list of SQLAlchemy BinaryExpression
            instances representing the filters.
        """

        type_filters = [
            i[0].ilike(str(i[1]).replace("*", "%")) for i in type_values if i[1]
        ]
        return type_filters
