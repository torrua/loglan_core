"""
This module provides a mechanism to extract words
from a database based on various criteria such as
event, key, type, and name through the WordSelector class.
"""

from __future__ import annotations

from functools import wraps
from typing import Type, cast, Iterable

from sqlalchemy import and_, select, join, Select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression

from loglan_core import t_connect_words
from loglan_core.addons.base_selector import BaseSelector
from loglan_core.addons.definition_selector import DefinitionSelector
from loglan_core.addons.utils import filter_word_by_event_id
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


class WordSelector(BaseSelector):  # pylint: disable=too-many-ancestors
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

    def with_relationships(self, selected: Iterable[str] | None = None) -> WordSelector:
        """
        Adds relationships to the query.

        Args:
            selected (set[str]): A set of relationship names to include.
            Defaults to None if all relationships should be included.

        Returns:
            WordSelector: A query with the relationships added.
        """
        available_relationships = {
            attr: getattr(self.class_, attr) for attr in self.class_.relationships()
        }
        relationships = {
            selectinload(v)
            for k, v in available_relationships.items()
            if not selected or k in selected
        }
        return cast(WordSelector, self.options(*relationships))

    @order_by_name
    def by_event(self, event_id: int | None = None) -> WordSelector:
        """
        Applies a filter to select words associated with a specific event.

        Args:
            event_id (int | None): The id of the event to filter by. Defaults to None.

        Returns:
            WordSelector: A query with the filter applied.
        """
        return cast(WordSelector, self.where(filter_word_by_event_id(event_id)))

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
        name = str(name).replace("*", "%")
        statement = (
            (
                self.class_.name.op("GLOB")(name)
                if self.is_sqlite
                else self.class_.name.like(name)
            )
            if case_sensitive
            else self.class_.name.ilike(name)
        )
        return cast(WordSelector, self.where(statement))

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
        return cast(WordSelector, self.where(self.class_.id.in_(subquery)))

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
                E.g. "2-Cpx", "C-Prim", "LW"

            type_x (str | None): The extended type to filter by. Defaults to None.
                E.g. "Predicate", "Name", "Affix"

            group (str | None): The group to filter by. Defaults to None.
                E.g. "Cpx", "Prim", "Little"

        Returns:
            WordSelector: A query with the filter applied.
        """
        if isinstance(type_, BaseType):
            return cast(
                WordSelector, self.join(BaseType).where(BaseType.id == type_.id)
            )

        type_values: tuple[tuple[InstrumentedAttribute, str | None | BaseType], ...] = (
            (BaseType.type_, type_),
            (BaseType.type_x, type_x),
            (BaseType.group, group),
        )

        type_filters = self.type_filters(type_values)

        return cast(
            WordSelector,
            (
                self
                if not type_filters
                else self.join(BaseType).where(and_(*type_filters))
            ),
        )

    @order_by_name
    def get_derivatives_of(self, word_id: int) -> WordSelector:
        """
        Selects all words that are derived from the given word.

        Args:
            word_id (int): The id of the word to filter by.

        Returns:
            WordSelector: A query with the filter applied.
        """
        return cast(
            WordSelector,
            self.where(
                self.class_.id.in_(self._select_derivative_ids_subquery(word_id))
            ),
        )

    @order_by_name
    def get_affixes_of(self, word_id: int) -> WordSelector:
        """
        Selects all affixes that are derived from the given word.

        Args:
            word_id (int): The id of the word to filter by.

        Returns:
            WordSelector: A query with the filter applied.
        """
        return cast(
            WordSelector, self.get_derivatives_of(word_id).by_type(type_x="Affix")
        )

    @order_by_name
    def get_complexes_of(self, word_id: int) -> WordSelector:
        """
        Selects all complexes that are derived from the given word.

        Args:
            word_id (int): The id of the word to filter by.

        Returns:
            WordSelector: A query with the filter applied.
        """
        return cast(WordSelector, self.get_derivatives_of(word_id).by_type(group="Cpx"))

    @property
    def inherit_cache(self):  # pylint: disable=missing-function-docstring
        return True

    def _select_derivative_ids_subquery(self, word_id: int) -> Select:
        # TODO Move to derivatives
        """
        Selects the ids of all words that are derived from the given word.

        Args:
            word_id (int): The id of the word to filter by.

        Returns:
            Select: A subquery that selects the ids of all words that are
            derived from the given word.
        """
        return (
            select(self.class_.id)
            .select_from(
                join(
                    t_connect_words,
                    self.class_,
                    t_connect_words.c.child_id == self.class_.id,
                )
            )
            .where(t_connect_words.c.parent_id == word_id)
        )

    @staticmethod
    def type_filters(type_values: tuple) -> list[BinaryExpression]:
        """
        Builds a collection of type filters based on provided type values.

        Args:
            type_values (tuple): A tuple containing values for type_, type_x, and group.

        Returns:
            list[BinaryExpression]: A list of SQLAlchemy BinaryExpression
            instances representing the filters.
        """

        type_filters = [
            i[0].ilike(str(i[1]).replace("*", "%")) for i in type_values if i[1]
        ]
        return type_filters

    @order_by_name
    def by_attributes(self, **kwargs) -> WordSelector:  # TODO Improve and verify
        """
        Selects all words by a set of attributes.

        Args:
            **kwargs: A set of attributes to filter by.

        Returns:
            WordSelector: A query with the filter applied.
        """
        return cast(WordSelector, self.where(self.filter_word_by_attributes(**kwargs)))

    def filter_word_by_attributes(self, **kwargs):
        """
        Generate a filter for a set of attributes.

        Args:
            **kwargs: A set of attributes to filter by.

        Returns:
            BinaryExpression: A filter expression for the given attributes.
        """
        return and_(*[getattr(self.class_, k) == v for k, v in kwargs.items()])
