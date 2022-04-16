# -*- coding: utf-8 -*-
"""
This module contains a basic Definition Model
"""
from typing import Union

from sqlalchemy import select
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session

from loglan_core.table_names import T_NAME_WORDS, T_NAME_DEFINITIONS
from loglan_core.connect_tables import t_connect_keys
from loglan_core.key import BaseKey
from loglan_core.base import BaseModel


__pdoc__ = {
    'BaseDefinition.created': False, 'BaseDefinition.updated': False,
}


class BaseDefinition(BaseModel):
    """BaseDefinition model"""
    __tablename__ = T_NAME_DEFINITIONS

    def __init__(
            self, word_id, position,
            usage, grammar_code, slots,
            case_tags, body, language, notes):
        super().__init__()
        self.word_id = word_id
        self.position = position
        self.usage = usage
        self.grammar_code = grammar_code
        self.slots = slots
        self.case_tags = case_tags
        self.body = body
        self.language = language
        self.notes = notes

    word_id = Column(Integer, ForeignKey(f'{T_NAME_WORDS}.id'), nullable=False)
    position = Column(Integer, nullable=False)
    usage = Column(String(64))
    grammar_code = Column(String(8))
    slots = Column(Integer)
    case_tags = Column(String(16))
    body = Column(Text, nullable=False)
    language = Column(String(16))
    notes = Column(String(255))

    APPROVED_CASE_TAGS = ["B", "C", "D", "F", "G", "J", "K", "N", "P", "S", "V", ]
    KEY_PATTERN = r"(?<=\«)(.+?)(?=\»)"

    _keys = relationship(
        BaseKey.__name__, secondary=t_connect_keys,
        back_populates="_definitions", lazy='dynamic')

    _source_word = relationship(
        "BaseWord", back_populates="_definitions")

    @property
    def keys_query(self):
        """

        Returns:

        """
        return self._keys

    @property
    def keys(self):
        """

        Returns:

        """
        return self.keys_query.all()

    @property
    def source_word(self):
        """

        Returns:

        """
        return self._source_word

    @property
    def grammar(self) -> str:
        """
        Combine definition's 'slots' and 'grammar_code' attributes

        Returns:
            String with grammar data like (3v) or (2n)
        """
        return f"({self.slots if self.slots else ''}" \
               f"{self.grammar_code if self.grammar_code else ''})"

    @classmethod
    def by_key(
            cls, session: Session, key: Union[BaseKey, str],
            language: str = None,
            case_sensitive: bool = False):
        """Definition.Query filtered by specified key

        Args:
          session:
          key: Union[BaseKey, str]:
          language: str: Language of key (Default value = None)
          case_sensitive: bool:  (Default value = False)

        Returns:
          BaseQuery

        """

        key = (BaseKey.word if isinstance(key, BaseKey) else str(key)).replace("*", "%")

        statement = select(cls).join(t_connect_keys).\
            join(BaseKey, BaseKey.id == t_connect_keys.c.KID)

        if language:
            statement = statement.filter(BaseKey.language == language)

        statement = statement.filter(
            BaseKey.word.like(key) if case_sensitive else BaseKey.word.ilike(key))

        return session.execute(statement.order_by(BaseKey.word)).scalars().all()
