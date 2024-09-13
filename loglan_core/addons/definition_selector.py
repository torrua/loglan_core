"""
This module provides the DefinitionSelector class which is a Selector for the BaseDefinition object.

The DefinitionSelector class allows for querying and filtering of BaseDefinition objects based on
various parameters such as event, key, and language. It is a subclass of the Select class.

Classes:
    DefinitionSelector: A selector model for the BaseDefinition object, it allows for querying and
    filtering of BaseDefinition objects.
"""

from __future__ import annotations

from typing import Type

from sqlalchemy import select, true
from typing_extensions import Self

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
        model: The class to be used as the returned object.
        is_sqlite: Boolean specifying if the object is being used with SQLite or not.
    """

    def __init__(
        self,
        model: Type[BaseDefinition] = BaseDefinition,
        is_sqlite: bool = False,
        case_sensitive: bool = False,
        disable_model_check: bool = False,
    ):
        """
        Initializes the DefinitionSelector object with the provided parameters.

        Args:
            model (Type[BaseDefinition]): The class to be used as the base key.
                Must be a subclass of BaseDefinition.
            is_sqlite (bool): If SQLite is being used. Defaults to False.
            case_sensitive (bool): If the queries should be case-sensitive.
            disable_model_check (bool): If the model check is disabled during initialization.

        Raises:
            ValueError: If the provided model is not a subclass of BaseDefinition.
        """

        super().__init__(model, is_sqlite, case_sensitive, disable_model_check)
        if not disable_model_check:
            self._is_model_accepted(model, BaseDefinition)

        self.model = model

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
            select(self.model.id)
            .join(t_connect_keys)
            .join(BaseWord)
            .where(filter_word_by_event_id(event_id))
            .scalar_subquery()
        )
        self._statement = self._statement.where(self.model.id.in_(subquery))
        return self

    def by_key(
        self,
        key: BaseKey | str,
        language: str | None = None,
    ) -> Self:
        """
        This method filters the definitions by the provided key, language and case sensitivity.

        Parameters:
            key (BaseKey | str): The key to filter by. Can be an instance of BaseKey or a string.
            language (str | None): The language to filter by.
            If None, no language filtering is applied.

        Returns:
            Self: The filtered DefinitionSelector instance with distinct keys.
        """

        search_key = key.word if isinstance(key, BaseKey) else str(key)
        filter_key = filter_key_by_word_cs(
            search_key, self.case_sensitive, self.is_sqlite
        )
        filter_language = filter_key_by_language(
            key.language if isinstance(key, BaseKey) else language
        )

        if hasattr(self.model, "keys"):
            self._statement = (
                self._statement.join(self.model.keys)
                .where(filter_key, filter_language)
                .distinct()
            )
        else:
            raise AttributeError(
                f"{self.model.__name__} does not have a 'keys' attribute"
            )

        return self

    def by_language(self, language: str | None = None) -> Self:
        """
        This method filters the definitions by the given language.

        Parameters:
            language (str | None): The language to filter by. If None,
                                   no language filtering is applied.

        Returns:
            Self: The filtered DefinitionSelector instance.
        """
        if hasattr(self.model, "language"):
            filter_language = self.model.language == language if language else true()
        else:
            raise AttributeError(
                f"{self.model.__name__} does not have a 'language' attribute"
            )
        self._statement = self._statement.where(filter_language)

        return self
