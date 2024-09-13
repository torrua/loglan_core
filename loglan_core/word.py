"""
This module contains a basic Word Model
"""

from __future__ import annotations

import datetime

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship

from loglan_core.author import BaseAuthor
from loglan_core.base import BaseModel
from loglan_core.base import str_008, str_064, str_128
from loglan_core.connect_tables import (
    t_connect_authors,
    t_connect_words,
)
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
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
        "type",
        ForeignKey(f"{T_NAME_TYPES}.id"),
        nullable=False,
    )

    type: Mapped[BaseType] = relationship(
        foreign_keys=[type_id],
        back_populates="words",
        lazy="joined",  # required for proper loading affixes and complexes
    )

    event_start_id: Mapped[int] = mapped_column(
        "event_start",
        ForeignKey(f"{T_NAME_EVENTS}.event_id"),
        nullable=False,
    )

    event_start: Mapped[BaseEvent] = relationship(
        foreign_keys=[event_start_id],
        back_populates="appeared_words",
    )

    event_end_id: Mapped[int | None] = mapped_column(
        "event_end",
        ForeignKey(
            f"{T_NAME_EVENTS}.event_id",
        ),
    )

    event_end: Mapped[BaseEvent | None] = relationship(
        foreign_keys=[event_end_id],
        back_populates="deprecated_words",
    )

    authors: Mapped[list[BaseAuthor]] = relationship(
        secondary=t_connect_authors,
        back_populates="contribution",
    )

    definitions: Mapped[list[BaseDefinition]] = relationship(
        back_populates="source_word",
    )

    # word's derivatives
    derivatives: Mapped[list[BaseWord]] = relationship(
        secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.parent_id == id),
        secondaryjoin=(t_connect_words.c.child_id == id),
        back_populates="parents",
    )

    # word's parents
    parents: Mapped[list[BaseWord]] = relationship(
        secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.child_id == id),
        secondaryjoin=(t_connect_words.c.parent_id == id),
        back_populates="derivatives",
    )

    @hybrid_property
    def affixes(self) -> list[BaseWord]:
        """
        Hybrid property that returns a list of affixes that are derived from the word.

        This property is a hybrid of a Python property and a SQLAlchemy expression.
        It can be used as a property in Python code or as a column in a SQLAlchemy query.

        Returns:
            list[BaseWord]: A list of affixes that are derived from the word.
        """
        return [child for child in self.derivatives if child.type.type_x == "Affix"]

    @hybrid_property
    def complexes(self) -> list[BaseWord]:
        """Hybrid property that returns a list of complexes derived from the word.

        This property is a hybrid of a Python property and a SQLAlchemy expression.
        It can be used as a property in Python code or as a column in a SQLAlchemy query.

        Returns:
            list[BaseWord]: A list of complexes derived from the word.
        """
        return [child for child in self.derivatives if child.type.group == "Cpx"]
