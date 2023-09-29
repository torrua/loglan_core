# -*- coding: utf-8 -*-
"""
This module contains a basic Definition Model
"""
from sqlalchemy import ForeignKey, Text
from sqlalchemy import select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from loglan_core.base import BaseModel, str_008, str_016, str_064, str_255
from loglan_core.connect_tables import t_connect_keys
from loglan_core.key import BaseKey
from loglan_core.table_names import T_NAME_WORDS, T_NAME_DEFINITIONS

__pdoc__ = {
    "BaseDefinition.created": False,
    "BaseDefinition.updated": False,
}


class BaseDefinition(BaseModel):
    """BaseDefinition model"""

    __tablename__ = T_NAME_DEFINITIONS

    def __init__(
        self,
        word_id: Mapped[int],
        position: Mapped[int],
        body: Mapped[str],
        usage: Mapped[str_064] | None = None,
        grammar_code: Mapped[str_008] | None = None,
        slots: Mapped[int] | None = None,
        case_tags: Mapped[str_016] | None = None,
        language: Mapped[str_016] | None = None,
        notes: Mapped[str_255] | None = None,
    ):
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

    def __repr__(self):
        """
        Returns:
        """
        return (
            f"<{self.__class__.__name__}"
            f"{' ID ' + str(self.id) + '/' if self.id else ' '}"
            f"{self.word_id} - {self.body[:20]}...>"
        )

    word_id: Mapped[int] = mapped_column(
        ForeignKey(f"{T_NAME_WORDS}.id"), nullable=False
    )
    position: Mapped[int] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    usage: Mapped[str_064 | None]
    grammar_code: Mapped[str_008 | None]
    slots: Mapped[int | None]
    case_tags: Mapped[str_016 | None]
    language: Mapped[str_016 | None]
    notes: Mapped[str_255 | None]

    APPROVED_CASE_TAGS = ("B", "C", "D", "F", "G", "J", "K", "N", "P", "S", "V")
    KEY_PATTERN = r"(?<=\«)(.+?)(?=\»)"

    _keys: Mapped[list[BaseKey]] = relationship(
        BaseKey.__name__,
        secondary=t_connect_keys,
        back_populates="_definitions",
        lazy="dynamic",
    )

    _source_word: Mapped["BaseWord"] = relationship(  # type: ignore
        "BaseWord",
        back_populates="_definitions",
    )

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
        return (
            f"({self.slots if self.slots else ''}"
            f"{self.grammar_code if self.grammar_code else ''})"
        )

    @classmethod
    def by_key(
        cls,
        key: BaseKey | str,
        language: str | None = None,
        case_sensitive: bool = False,
    ):
        """Definition.Query filtered by specified key

        Args:
          key: Union[BaseKey, str]:
          language: str: Language of key (Default value = None)
          case_sensitive: bool:  (Default value = False)

        Returns:
          BaseQuery

        """

        search_key = (
            BaseKey.word if isinstance(key, BaseKey) else str(key).replace("*", "%")
        )

        statement = (
            select(cls)
            .join(t_connect_keys)
            .join(BaseKey, BaseKey.id == t_connect_keys.c.KID)
        )

        if language:
            statement = statement.filter(BaseKey.language == language)

        statement = statement.filter(
            BaseKey.word.like(search_key)
            if case_sensitive
            else BaseKey.word.ilike(search_key)
        )

        return statement
