"""
This module contains a basic Key Model
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship

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

    word: Mapped[str_064] = mapped_column(nullable=False)
    """*Key's vernacular word*  
        **str** : max_length=64, nullable=False, unique=False  
    It is non-unique, as words can be the same in spelling in different languages"""
    language: Mapped[str_016] = mapped_column(nullable=False)
    """*Key's language*  
        **str** : max_length=16, nullable=False, unique=False"""

    definitions: Mapped[list[BaseDefinition]] = relationship(
        secondary=t_connect_keys,
        back_populates="keys",
    )
