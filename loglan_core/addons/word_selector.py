"""
This module provides a mechanism to extract words
from a database based on various criteria such as
event, key, type, and name through the WordSelector class.
"""

from __future__ import annotations

from functools import wraps
from typing import Type

from sqlalchemy import and_, select
from typing_extensions import Self

from loglan_core.addons.base_selector import BaseSelector
from loglan_core.addons.definition_selector import DefinitionSelector
from loglan_core.addons.utils import filter_word_by_event_id
from loglan_core.connect_tables import t_connect_words
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
        result._statement = result.get_statement().order_by(result.model.name)
        return result

    return wrapper


class WordSelector(BaseSelector):  # pylint: disable=too-many-ancestors
    """
    Class to extract words from a database based on various criteria.

    Extends the SQLAlchemy Select class to provide additional functionality.
    """

    def __init__(
        self,
        model: Type = BaseWord,
        is_sqlite: bool = False,
        case_sensitive: bool = False,
    ):
        """
        Initialize a WordSelector instance.

        Args:
            is_sqlite (bool): If SQLite is being used. Defaults to False.
        """

        super().__init__(model, is_sqlite, case_sensitive)

    @order_by_name
    def by_event(self, event_id: int | None = None) -> Self:
        """
        Applies a filter to select words associated with a specific event.

        Args:
            event_id (int | None): The id of the event to filter by. Defaults to None.

        Returns:
            Self: A query with the filter applied.
        """
        self._statement = self._statement.where(filter_word_by_event_id(event_id))
        return self

    def by_name(
        self,
        name: str,
    ) -> Self:
        """
        Applies a filter to select words by a specific name.

        Args:
            name (str): The name to filter by.
            Defaults to False.
        Returns:
            Self: A query with the filter applied.
        """

        return self.filter_by(name=name)

    def by_key(
        self,
        key: BaseKey | str,
        language: str | None = None,
        case_sensitive: bool = False,
    ) -> Self:
        """
        Applies a filter to select words by a specific key.

        Args:
            key (BaseKey | str): The key to filter by.
            It can either be an instance of BaseKey or a string.
            language (str | None): The language of the key. Defaults to None.
            case_sensitive (bool): Whether the search should be case-sensitive.
                Defaults to False.

        Returns:
            Self: A query with the filter applied.
        """

        definition_query = DefinitionSelector(is_sqlite=self.is_sqlite).by_key(
            key=key,
            language=language,
            case_sensitive=case_sensitive,
        )
        subquery = select(definition_query._statement.subquery().c.word_id)
        self._statement = self._statement.where(self.model.id.in_(subquery))
        return self

    @order_by_name
    def by_type(
        self,
        type_: BaseType | str | None = None,
        type_x: str | None = None,
        group: str | None = None,
    ) -> Self:
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
            Self: A query with the filter applied.
        """
        if isinstance(type_, BaseType):
            self._statement = self._statement.join(BaseType).where(
                BaseType.id == type_.id
            )
            return self

        type_values = (
            (BaseType.type_, type_),
            (BaseType.type_x, type_x),
            (BaseType.group, group),
        )

        type_filters = [
            i[0].ilike(str(i[1]).replace("*", "%")) for i in type_values if i[1]
        ]

        if not type_filters:
            return self

        self._statement = self._statement.join(BaseType).where(and_(*type_filters))
        return self

    @order_by_name
    def get_derivatives_of(self, word_id: int) -> Self:
        """
        Selects all words that are derived from the given word.

        Args:
            word_id (int): The id of the word to filter by.

        Returns:
            Self: A query with the filter applied.
        """

        derivative_ids_subquery = select(t_connect_words.c.child_id).where(
            t_connect_words.c.parent_id == word_id
        )

        return self.where(self.model.id.in_(derivative_ids_subquery))

    def get_affixes_of(self, word_id: int) -> Self:
        """
        Selects all affixes that are derived from the given word.

        Args:
            word_id (int): The id of the word to filter by.

        Returns:
            Self: A query with the filter applied.
        """
        return self.get_derivatives_of(word_id).by_type(type_x="Affix")

    def get_complexes_of(self, word_id: int) -> Self:
        """
        Selects all complexes that are derived from the given word.

        Args:
            word_id (int): The id of the word to filter by.

        Returns:
            Self: A query with the filter applied.
        """
        return self.get_derivatives_of(word_id).by_type(group="Cpx")

    @property
    def inherit_cache(self):  # pylint: disable=missing-function-docstring
        return True
