"""
This module provides a mechanism to extract words
from a database based on various criteria such as
event, key, type, and name through the WordSelector class.
"""

from __future__ import annotations

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


class WordSelector(BaseSelector):  # pylint: disable=too-many-ancestors
    """
    Class to extract words from a database based on various criteria.

    Extends the SQLAlchemy Select class to provide additional functionality.
    """

    def __init__(
        self,
        model: Type[BaseWord] = BaseWord,
        is_sqlite: bool = False,
        case_sensitive: bool = False,
        disable_model_check: bool = False,
    ):
        """
        Initializes the WordSelector object with the provided parameters.

        Args:
            model (Type[BaseWord]): The class to be used as the base key.
                Must be a subclass of BaseWord.
            is_sqlite (bool): If SQLite is being used. Defaults to False.
            case_sensitive (bool): If the queries should be case-sensitive.
            disable_model_check (bool): If the model check is disabled during initialization.

        Raises:
            ValueError: If the provided model is not a subclass of BaseWord.
        """

        super().__init__(
            model=model,
            is_sqlite=is_sqlite,
            case_sensitive=case_sensitive,
            disable_model_check=disable_model_check,
        )

        if not self.disable_model_check:
            self._is_model_accepted(model, BaseWord)

        self.model = model

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
        if hasattr(self.model, "name"):
            condition = self.get_like_condition(self.model.name, name)
        else:
            raise AttributeError(
                f"{self.model.__name__} does not have a 'name' attribute"
            )

        self._statement = self._statement.where(condition)
        return self

    def by_key(
        self,
        key: BaseKey | str,
        language: str | None = None,
    ) -> Self:
        """
        Applies a filter to select words by a specific key.

        Args:
            key (BaseKey | str): The key to filter by.
            It can either be an instance of BaseKey or a string.
            language (str | None): The language of the key. Defaults to None.
                Defaults to False.

        Returns:
            Self: A query with the filter applied.
        """

        definition_query = DefinitionSelector(
            is_sqlite=self.is_sqlite,
            case_sensitive=self.case_sensitive,
        ).by_key(
            key=key,
            language=language,
        )
        subquery = select(definition_query.get_statement().subquery().c.word_id)
        self._statement = self._statement.where(self.model.id.in_(subquery))
        return self

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
            self._statement = self._statement
            return self

        self._statement = self._statement.join(BaseType).where(and_(*type_filters))
        return self

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

        self._statement = self._statement.where(
            self.model.id.in_(derivative_ids_subquery)
        )
        return self

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
