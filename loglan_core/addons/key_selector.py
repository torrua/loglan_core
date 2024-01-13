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

from sqlalchemy import select

from loglan_core.addons.base_selector import BaseSelector
from loglan_core.connect_tables import t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.key import BaseKey
from loglan_core.word import BaseWord


class KeySelector(BaseSelector):  # pylint: disable=too-many-ancestors
    """
    A class used to select keys meeting certain criteria.

    Attributes:
        class_ (Type[BaseKey]): The class to be used as the base key.
            Must be a subclass of BaseKey.
        is_sqlite (bool): Indicator if the object is being used with SQLite or not.
    """

    def __init__(self, class_=BaseKey, is_sqlite: bool = False) -> None:
        """
        Initializes the KeySelector object with the provided parameters.

        Args:
            class_ (Type[BaseKey]): The class to be used as the base key.
                Must be a subclass of BaseKey.
            is_sqlite (bool): Indicator if the object is being used with SQLite or not.

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
    def inherit_cache(self):  # pylint: disable=C0116
        """
        Returns:
             bool
        """
        return True

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
        Filters the keys by the given key.

        Args:
            key (str): The key to filter by.
            case_sensitive (bool): Determines whether the key search should be
                case-sensitive. Defaults to False.

        Returns:
            KeySelector: The filtered KeySelector instance.
        """
        return self.where(
            self.class_.filter_by_key_cs(key, case_sensitive, self.is_sqlite)
        )

    def by_language(self, language: str | None = None) -> KeySelector:
        """
        Filters the keys by the given language.

        Args:
            language (str | None): The language to filter by.
                If None, no language filtering is applied.

        Returns:
            KeySelector: The filtered KeySelector instance.
        """
        return self.where(self.class_.filter_by_language(language))
