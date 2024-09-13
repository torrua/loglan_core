"""
This module provides the `KeySelector` class, which inherits from `Select`
and provides methods for filtering keys based on certain criteria.

The KeySelector class has methods to filter keys by event ID, key, and language.
Each method returns a new instance of KeySelector with the applied filters.

The KeySelector class is initialized with a class object and a boolean
indicating if it is being used with SQLite. The class object must be
a subclass of BaseKey.

Classes:
    KeySelector: A class used to select keys meeting certain criteria.

Example:
    key_selector = KeySelector(MyKeyClass)
    filtered_by_event = key_selector.by_event(1)
    filtered_by_key = key_selector.by_key('mykey')
    filtered_by_language = key_selector.by_language('English')

This allows for flexible and powerful querying of keys in a codebase.
"""

from __future__ import annotations

from typing import Type

from sqlalchemy import select

from loglan_core.addons.base_selector import BaseSelector
from loglan_core.addons.utils import (
    filter_word_by_event_id,
    filter_key_by_word_cs,
    filter_key_by_language,
)
from loglan_core.connect_tables import t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.key import BaseKey
from loglan_core.word import BaseWord


class KeySelector(BaseSelector):  # pylint: disable=too-many-ancestors
    """
    A class used to select keys meeting certain criteria.

    Attributes:
        model (Type[BaseKey]): The class to be used as the base key.
            Must be a subclass of BaseKey.
        is_sqlite (bool): If SQLite is being used. Defaults to False.
        case_sensitive (bool): If the queries should be case-sensitive.
        disable_model_check (bool): If the model check is disabled during initialization.
    """

    def __init__(
        self,
        model: Type[BaseKey] = BaseKey,
        is_sqlite: bool = False,
        case_sensitive: bool = False,
        disable_model_check: bool = False,
    ) -> None:
        """
        Initializes the KeySelector object with the provided parameters.

        Args:
            model (Type[BaseKey]): The class to be used as the base key.
                Must be a subclass of BaseKey.
            is_sqlite (bool): If SQLite is being used. Defaults to False.
            case_sensitive (bool): If the queries should be case-sensitive.
            disable_model_check (bool): If the model check is disabled during initialization.

        Raises:
            ValueError: If the provided model is not a subclass of BaseKey.
        """

        super().__init__(model, is_sqlite, case_sensitive, disable_model_check)

        if not self.disable_model_check:
            self._is_model_accepted(model, BaseKey)

        self.model = model

    def by_event(self, event_id: int | None = None) -> KeySelector:
        """
        Filters the keys by the given event ID.

        Args:
            event_id (int | None): The identifier of the event to filter by.
                If None, no event filtering is applied.

        Returns:
            KeySelector: The filtered KeySelector instance.
        """

        subquery = (
            select(self.model.id)
            .join(t_connect_keys)
            .join(BaseDefinition)
            .join(BaseWord)
            .where(filter_word_by_event_id(event_id))
            .scalar_subquery()
        )
        self._statement = self._statement.where(self.model.id.in_(subquery))
        return self

    def by_key(self, key: str) -> KeySelector:
        """
        Filters the keys by the given key.

        Args:
            key (str): The key to filter by.

        Returns:
            KeySelector: The filtered KeySelector instance.
        """
        self._statement = self._statement.where(
            filter_key_by_word_cs(key, self.case_sensitive, self.is_sqlite)
        )
        return self

    def by_language(self, language: str | None = None) -> KeySelector:
        """
        Filters the keys by the given language.

        Args:
            language (str | None): The language to filter by.
                If None, no language filtering is applied.

        Returns:
            KeySelector: The filtered KeySelector instance.
        """
        self._statement = self._statement.where(filter_key_by_language(language))
        return self

    def by_word_id(self, word_id: int) -> KeySelector:
        """
        Filters the keys by the given word ID.

        Args:
            word_id (int): The identifier of the word to filter by.

        Returns:
            KeySelector: The filtered KeySelector instance.

        Keep in mind that duplicated keys from related definitions
        will be counted with ```.count()``` but excluded from ```.all()``` request

        """
        self._statement = (
            self._statement.distinct()
            .join(t_connect_keys)
            .join(BaseDefinition, BaseDefinition.id == t_connect_keys.c.DID)
            .join(BaseWord, BaseWord.id == BaseDefinition.word_id)
            .filter(BaseWord.id == word_id)
            .order_by(BaseKey.word.asc())
        )
        return self
