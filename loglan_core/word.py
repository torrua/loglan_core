"""
This module contains a basic Word Model
"""

from __future__ import annotations

import datetime

from sqlalchemy import ForeignKey, JSON
from sqlalchemy import select
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from loglan_core.author import BaseAuthor
from loglan_core.base import BaseModel
from loglan_core.base import str_008, str_064, str_128
from loglan_core.connect_tables import (
    t_connect_authors,
    t_connect_words,
    t_connect_keys,
)
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
from loglan_core.key import BaseKey
from loglan_core.table_names import T_NAME_EVENTS, T_NAME_TYPES, T_NAME_WORDS
from loglan_core.type import BaseType

__pdoc__ = {
    "BaseWord.created": False,
    "BaseWord.updated": False,
}


class BaseWord(BaseModel):
    """BaseWord model"""

    __tablename__ = T_NAME_WORDS

    def __init__(
        self,
        id_old: Mapped[int],
        name: Mapped[str_064],
        type_id: Mapped[int],
        event_start_id: Mapped[int],
        event_end_id: Mapped[int] | None = None,
        tid_old: Mapped[int] | None = None,
        origin: Mapped[str_128] | None = None,
        origin_x: Mapped[str_064] | None = None,
        match: Mapped[str_008] | None = None,
        rank: Mapped[str_008] | None = None,
        year: Mapped[datetime.date] | None = None,
        notes: Mapped[dict] | None = None,
    ):
        """
        Returns:
        """
        super().__init__()

        self.id_old = id_old
        self.name = name
        self.type_id = type_id
        self.event_start_id = event_start_id

        self.event_end_id = event_end_id
        self.tid_old = tid_old

        self.origin = origin
        self.origin_x = origin_x
        self.match = match
        self.rank = rank
        self.year = year

        self.notes = notes

    def __str__(self):
        """
        Returns:
        """
        return (
            f"<{self.__class__.__name__}"
            f"{' ID ' + str(self.id) + ' ' if self.id else ' '}"
            f"{self.name}>"
        )

    id: Mapped[int] = mapped_column(primary_key=True)
    """Word's internal ID number: Integer"""

    name: Mapped[str_064] = mapped_column(nullable=False)
    origin: Mapped[str_128 | None]
    origin_x: Mapped[str_064 | None]
    match: Mapped[str_008 | None]
    rank: Mapped[str_008 | None]
    year: Mapped[datetime.date | None]
    notes: Mapped[dict[str, str] | None] = mapped_column(JSON)

    # Field for legacy database compatibility
    id_old: Mapped[int] = mapped_column(nullable=False)
    tid_old: Mapped[int | None] = mapped_column("TID_old")  # references

    # Relationships
    type_id: Mapped[int] = mapped_column(
        "type", ForeignKey(f"{T_NAME_TYPES}.id"), nullable=False
    )

    relationship_type: Mapped[BaseType] = relationship(
        back_populates="relationship_words"
    )

    @property
    def type(self) -> BaseType:
        """
        Returns:
        """
        return self.relationship_type

    event_start_id: Mapped[int] = mapped_column(
        "event_start", ForeignKey(f"{T_NAME_EVENTS}.event_id"), nullable=False
    )

    relationship_event_start: Mapped[BaseEvent] = relationship(
        foreign_keys=[event_start_id], back_populates="relationship_appeared_words"
    )

    @property
    def event_start(self) -> BaseEvent:
        """
        Returns:
        """
        return self.relationship_event_start

    event_end_id: Mapped[int | None] = mapped_column(
        "event_end", ForeignKey(f"{T_NAME_EVENTS}.event_id")
    )

    relationship_event_end: Mapped[BaseEvent | None] = relationship(
        foreign_keys=[event_end_id], back_populates="relationship_deprecated_words"
    )

    @property
    def event_end(self) -> BaseEvent | None:
        """
        Returns:
        """
        return self.relationship_event_end

    relationship_authors: Mapped[list[BaseAuthor]] = relationship(
        secondary=t_connect_authors,
        back_populates="relationship_contribution",
        lazy="dynamic",
        enable_typechecks=False,
    )

    @property
    def authors_query(self):
        """
        Returns:
        """
        return self.relationship_authors

    @property
    def authors(self) -> list[BaseAuthor]:
        """
        Returns:
        """
        return self.authors_query.all()

    relationship_definitions: Mapped[list[BaseDefinition]] = relationship(
        back_populates="relationship_source_word",
        lazy="dynamic",
    )

    @property
    def definitions_query(self):
        """
        Returns:
        """
        return self.relationship_definitions

    @property
    def definitions(self) -> list[BaseDefinition]:
        """
        Returns:
        """
        return self.definitions_query.order_by(BaseDefinition.position.asc()).all()

    # word's derivatives
    relationship_derivatives: Mapped[list[BaseWord]] = relationship(
        secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.parent_id == id),
        secondaryjoin=(t_connect_words.c.child_id == id),
        backref=backref(
            "relationship_parents", lazy="dynamic", enable_typechecks=False
        ),
        lazy="dynamic",
        enable_typechecks=False,
    )

    @property
    def derivatives_query(self):
        """
        Returns:
        """
        return self.relationship_derivatives

    @property
    def derivatives(self):
        """
        Returns:
        """
        return self.derivatives_query.all()

    def derivatives_query_by(
        self,
        word_type: str | None = None,
        word_type_x: str | None = None,
        word_group: str | None = None,
        type_class=BaseType,
    ):
        """Query to get all derivatives of the word, depending on its parameters

        Args:
          word_type: str:  (Default value = None)
          E.g. "2-Cpx", "C-Prim", "LW"

          word_type_x: str:  (Default value = None)
          E.g. "Predicate", "Name", "Affix"

          word_group: str:  (Default value = None)
          E.g. "Cpx", "Prim", "Little"

          type_class:
        Returns:
            List[Word]
        """

        type_values = [
            (type_class.type, word_type),
            (type_class.type_x, word_type_x),
            (type_class.group, word_group),
        ]

        type_filters = [i[0] == i[1] for i in type_values if i[1]]

        return (
            self.derivatives_query.join(type_class)
            .filter(self.id == t_connect_words.c.parent_id, *type_filters)
            .order_by(type(self).name.asc())
        )

    @property
    def affixes(self):
        """
        Get all word's affixes if exist
        Only primitives have affixes.

        Returns:
            BaseQuery
        """
        return self.derivatives_query_by(word_type="Afx").all()

    @property
    def complexes(self):
        """
        Get all word's complexes if exist
        Only primitives and Little Words have complexes.

        Returns:
            BaseQuery
        """
        return self.derivatives_query_by(word_group="Cpx").all()

    @property
    def parents_query(self):
        """Query to get all parents for Complexes, Little words or Affixes

        Returns:
            BaseQuery
        """
        return self.relationship_parents  # pylint: disable=E1101

    @property
    def parents(self):
        """
        Returns:
        """
        return self.parents_query.all()

    @property
    def keys_query(self):
        """Get all BaseKey object related to this BaseWord.

        Keep in mind that duplicated keys from related definitions
        will be counted with ```.count()``` but excluded from ```.all()``` request

        Returns:
        """
        return (
            select(BaseKey)
            .join(t_connect_keys)
            .join(BaseDefinition, BaseDefinition.id == t_connect_keys.c.DID)
            .join(BaseWord, BaseWord.id == BaseDefinition.word_id)
            .filter(BaseWord.id == self.id)
            .order_by(BaseKey.word.asc())
        )

    @property
    def keys(self) -> list[BaseKey]:
        """
        Returns:
        """
        return sorted(set(key for d in self.definitions for key in d.keys_query.all()))

    @classmethod
    def filter_by_event_id(cls, event_id: int | None) -> BooleanClauseList:
        """
        Returns: BooleanClauseList
        """
        event_id_filter = event_id or BaseEvent.latest_id()
        start_id_condition = cls.event_start_id <= event_id_filter
        end_id_condition = (cls.event_end_id > event_id_filter) | cls.event_end_id.is_(None)
        return start_id_condition & end_id_condition

    @classmethod
    def filter_by_name_cs(
        cls,
        name: str,
        case_sensitive: bool = False,
        is_sqlite: bool = False,
    ) -> BinaryExpression:
        """
        case-sensitive name filter
        Returns: BinaryExpression
        """
        name = str(name).replace("*", "%")
        return (
            (cls.name.op("GLOB")(name) if is_sqlite else cls.name.like(name))
            if case_sensitive
            else cls.name.ilike(name)
        )
