"""
This module contains a basic Definition Model
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy import true
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import ColumnElement

from loglan_core.base import BaseModel, str_008, str_016, str_064, str_255
from loglan_core.connect_tables import t_connect_keys
from loglan_core.key import BaseKey
from loglan_core.table_names import T_NAME_WORDS, T_NAME_DEFINITIONS

if TYPE_CHECKING:
    from loglan_core.word import BaseWord

__pdoc__ = {
    "BaseDefinition.created": False,
    "BaseDefinition.updated": False,
}


class BaseDefinition(BaseModel):
    """
    The BaseDefinition model.

    Attributes:
        word_id (Mapped[int]): The ID of the word.
        position (Mapped[int]): The position of the word.
        body (Mapped[str]): The body of the word.
        usage (Mapped[str_064] | None): The usage of the word.
        grammar_code (Mapped[str_008] | None): The grammar code of the word.
        slots (Mapped[int] | None): The slots of the word.
        case_tags (Mapped[str_016] | None): The case tags of the word.
        language (Mapped[str_016] | None): The language of the word.
        notes (Mapped[str_255] | None): The notes of the word.
        APPROVED_CASE_TAGS (tuple): A tuple of approved case tags.
        KEY_PATTERN (str): The pattern for the key.
        relationship_keys (Mapped[list[BaseKey]]): The relationship of keys.
        relationship_source_word (Mapped["BaseWord"]): The relationship of source word.

    """

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

    def __str__(self):
        """
        String representation of the BaseDefinition object.

        Returns:
            str: A string representation of the object.
        """
        return (
            f"<{self.__class__.__name__}"
            f" ID {str(self.id)}/{self.word_id} {self.body[:20]}…>"
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

    relationship_keys: Mapped[list[BaseKey]] = relationship(
        BaseKey.__name__,
        secondary=t_connect_keys,
        back_populates="relationship_definitions",
        lazy="dynamic",
    )

    relationship_source_word: Mapped[BaseWord] = relationship(  # type: ignore
        "BaseWord",
        back_populates="relationship_definitions",
    )

    @property
    def keys_query(self):
        """
        Returns:
        """
        return self.relationship_keys

    @property
    def keys(self):
        """
        Get all keys related to the BaseDefinition.

        Returns:
            list[BaseKey]: All keys related to the BaseDefinition.
        """
        return self.keys_query.all()

    @property
    def source_word(self):
        """
        Get source word related to the BaseDefinition.

        Returns:
            BaseWord: Source word of the BaseDefinition.
        """
        return self.relationship_source_word

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
    def filter_language(cls, language: str | None = None) -> ColumnElement[bool]:
        """
        Filter by specified language.

        Args:
            language (str, optional): The language to filter by. Defaults to None.

        Returns:
            ColumnElement[bool]: The filtered query.
        """
        return cls.language == language if language else true()
