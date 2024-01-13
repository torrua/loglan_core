"""
This module contains a basic Key Model
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, true
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.expression import ColumnElement

from loglan_core.base import BaseModel, str_016, str_064
from loglan_core.connect_tables import t_connect_keys
from loglan_core.table_names import T_NAME_KEYS

if TYPE_CHECKING:
    from loglan_core.definition import BaseDefinition

__pdoc__ = {
    "BaseKey.definitions": """
    *Relationship query for getting a list of definitions related to this key*

    **query** : Optional[List[BaseDefinition]]""",
    "BaseKey.created": False,
    "BaseKey.updated": False,
}


class BaseKey(BaseModel):
    """Base Key's DB Model

    Describes a table structure for storing information
    about keywords of the word's definitions.
    Some keywords could belong to many definitions
    and some definitions could have many keywords.
    That's why the relationship between Key
    and Definition should be many-to-many. See `t_connect_keys`.

    There is additional `word_language` UniqueConstraint here.

    <details><summary>Show Examples</summary><p>
    ```python
    {'language': 'en', 'word': 'aura', 'id': 1234}

    {'language': 'en', 'word': 'emotionality', 'id': 4321}
    ```
    </p></details>
    """

    __tablename__ = T_NAME_KEYS
    __table_args__ = (UniqueConstraint("word", "language", name="_word_language_uc"),)

    def __init__(self, word, language):
        super().__init__()
        self.word = word
        self.language = language

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id} '{self.word}' ({self.language})>"

    def __lt__(self, other):
        return (self.word, self.id) < (other.word, other.id)

    word: Mapped[str_064] = mapped_column(nullable=False)
    """*Key's vernacular word*  
        **str** : max_length=64, nullable=False, unique=False  
    It is non-unique, as words can be the same in spelling in different languages"""
    language: Mapped[str_016] = mapped_column(nullable=False)
    """*Key's language*  
        **str** : max_length=16, nullable=False, unique=False"""

    relationship_definitions: Mapped[list[BaseDefinition]] = relationship(  # type: ignore
        secondary=t_connect_keys,
        back_populates="relationship_keys",
        lazy="dynamic",
    )

    @property
    def definitions_query(self):
        """
        Returns:
        """
        return self.relationship_definitions

    @property
    def definitions(self):
        """
        Returns:
        """
        return self.definitions_query.all()

    @classmethod
    def filter_by_key_cs(
        cls,
        key: str,
        case_sensitive: bool = False,
        is_sqlite: bool = False,
    ) -> BinaryExpression:
        """case sensitive name filter"""
        key = str(key).replace("*", "%")
        return (
            (cls.word.op("GLOB")(key) if is_sqlite else cls.word.like(key))
            if case_sensitive
            else cls.word.ilike(key)
        )

    @classmethod
    def filter_by_language(cls, language: str | None = None) -> ColumnElement[bool]:
        """
        Filter the language of the base key.

        Args:
            language (str or None): The language to filter by.
            If None, no language filter will be applied.

        Returns:
            ColumnElement[bool]: A filter condition for the base key's language.
        """
        return (cls.language == language) if language else true()
