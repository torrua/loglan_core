"""
This module provides the DefinitionSelector class which is a Selector for the BaseDefinition object.

The DefinitionSelector class allows for querying and filtering of BaseDefinition objects based on
various parameters such as event, key, and language. It is a subclass of the Select class.

Classes:
    DefinitionSelector: A selector model for the BaseDefinition object, it allows for querying and
    filtering of BaseDefinition objects.
"""

from __future__ import annotations

from sqlalchemy import select

from loglan_core.addons.base_selector import BaseSelector
from loglan_core.connect_tables import t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.key import BaseKey
from loglan_core.word import BaseWord


class DefinitionSelector(BaseSelector):  # pylint: disable=too-many-ancestors
    """
    This class is a selector model for the BaseDefinition object. It allows for
    querying and filtering of BaseDefinition objects based on various parameters
    such as event, key, and language. It is a subclass of the Select class.

    Methods:
        __init__: Initializes the DefinitionSelector object.
        inherit_cache: Property that always returns True.
        by_event: Returns a new DefinitionSelector object filtered by a specific event.
        by_key: Returns a BaseQuery object filtered by a specific key.
        by_language: Returns a new DefinitionSelector object filtered by a specific language.

    Raises:
        ValueError: If the provided class_ is not a subclass of BaseDefinition.

    Attributes:
        class_: The class to be used as the returned object.
        is_sqlite: Boolean specifying if the object is being used with SQLite or not.
    """

    def __init__(self, class_=BaseDefinition, is_sqlite: bool = False):
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
    def inherit_cache(self):  # pylint: disable=C0116
        """
        :return: bool
        """
        return True

    def by_event(self, event_id: int | None = None) -> DefinitionSelector:
        """
        This method filters the definitions by the given event id.

        Parameters:
            event_id (int | None): The id of the event to filter by. If None,
                                   no event filtering is applied.

        Returns:
            DefinitionSelector: The filtered DefinitionSelector instance.
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
        """
        This method filters the definitions by the provided key, language and case sensitivity.

        Parameters:
            key (BaseKey | str): The key to filter by. Can be an instance of BaseKey or a string.
            language (str | None): The language to filter by.
            If None, no language filtering is applied.
            case_sensitive (bool): Flag indicating whether filtering should be case sensitive.

        Returns:
            DefinitionSelector: The filtered DefinitionSelector instance with distinct keys.
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
        """
        This method filters the definitions by the given language.

        Parameters:
            language (str | None): The language to filter by. If None,
                                   no language filtering is applied.

        Returns:
            DefinitionSelector: The filtered DefinitionSelector instance.
        """
        return self.filter(self.class_.filter_language(language))
