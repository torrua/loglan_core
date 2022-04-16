# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a basic Key Model
"""
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship

from loglan_core.base import BaseModel
from loglan_core.connect_tables import t_connect_keys
from loglan_core.table_names import T_NAME_KEYS

__pdoc__ = {
    'BaseKey.definitions':
        """*Relationship query for getting a list of definitions related to this key*

    **query** : Optional[List[BaseDefinition]]""",
    'BaseKey.created': False, 'BaseKey.updated': False, }


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
    __table_args__ = (
        UniqueConstraint('word', 'language', name='_word_language_uc'), )

    def __init__(self, word, language):
        super().__init__()
        self.word = word
        self.language = language

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.word}' ({self.language})>"

    word = Column(String(64), nullable=False, unique=False)
    """*Key's vernacular word*  
        **str** : max_length=64, nullable=False, unique=False  
    It is non-unique, as words can be the same in spelling in different languages"""
    language = Column(String(16), nullable=False, unique=False)
    """*Key's language*  
        **str** : max_length=16, nullable=False, unique=False"""

    _definitions = relationship(
        "BaseDefinition", secondary=t_connect_keys, lazy='dynamic', back_populates="_keys")

    @property
    def definitions_query(self):
        """

        Returns:

        """
        return self._definitions

    @property
    def definitions(self):
        """

        Returns:

        """
        return self.definitions_query.all()
