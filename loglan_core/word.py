"""
This module contains a basic Word Model.
"""

from __future__ import annotations

import datetime

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship

from .author import BaseAuthor
from .base import BaseModel, str_008, str_064, str_128
from .connect_tables import (
    t_connect_authors,
    t_connect_words,
)
from .definition import BaseDefinition
from .event import BaseEvent
from .table_names import T_NAME_EVENTS, T_NAME_TYPES, T_NAME_WORDS
from .type import BaseType


class BaseWord(BaseModel):
    """BaseWord model representing a word in the database.

    Attributes:
        id (int): Word's internal ID number.
        name (str_064): The name of the word.
        origin (str_128 | None): The origin of the word.
        origin_x (str_064 | None): Additional origin information.
        match (str_008 | None): Matching criteria for the word.
        rank (str_008 | None): Rank of the word.
        year (datetime.date | None): Year associated with the word.
        notes (dict[str, str] | None): Additional notes about the word.
        id_old (int): Legacy ID for compatibility with older databases.
        tid_old (int | None): Legacy TID for compatibility.
        type_id (int): Foreign key referencing the type of the word.
        event_start_id (int): Foreign key referencing the start event.
        event_end_id (int | None): Foreign key referencing the end event.
        authors (list[BaseAuthor]): List of authors associated with the word.
        definitions (list[BaseDefinition]): List of definitions for the word.
        derivatives (list[BaseWord]): List of words derived from this word.
        parents (list[BaseWord]): List of parent words of this word.
    """

    __tablename__ = T_NAME_WORDS

    def __init__(  # pylint: disable=too-many-positional-arguments
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
        """Initializes a BaseWord instance.

        Args:
            id_old (int): Legacy ID for compatibility.
            name (str_064): The name of the word.
            type_id (int): Foreign key referencing the type of the word.
            event_start_id (int): Foreign key referencing the start event.
            event_end_id (int | None): Foreign key referencing the end event.
            tid_old (int | None): Legacy TID for compatibility.
            origin (str_128 | None): The origin of the word.
            origin_x (str_064 | None): Additional origin information.
            match (str_008 | None): Matching criteria for the word.
            rank (str_008 | None): Rank of the word.
            year (datetime.date | None): Year associated with the word.
            notes (dict | None): Additional notes about the word.
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
        """Returns a string representation of the BaseWord instance.

        Returns:
            str: A string representation of the BaseWord instance.
        """
        return (
            f"<{self.__class__.__name__}"
            f"{' ID ' + str(self.id) + ' ' if self.id else ' '}"
            f"{self.name}>"
        )

    id: Mapped[int] = mapped_column(primary_key=True)
    """Word's internal ID number: Integer"""

    name: Mapped[str_064] = mapped_column(nullable=False)
    """The name of the word: String with a maximum length of 64 characters."""

    origin: Mapped[str_128 | None]
    """The origin of the word: String with a maximum length of 128 characters or None."""

    origin_x: Mapped[str_064 | None]
    """Additional origin information: String with a maximum length of 64 characters or None."""

    match: Mapped[str_008 | None]
    """Matching criteria for the word: String with a maximum length of 8 characters or None."""

    rank: Mapped[str_008 | None]
    """Rank of the word: String with a maximum length of 8 characters or None."""

    year: Mapped[datetime.date | None]
    """Year associated with the word: Date or None."""

    notes: Mapped[dict[str, str] | None] = mapped_column(JSON)
    """Additional notes about the word: JSON-encoded dictionary or None."""

    # Field for legacy database compatibility
    id_old: Mapped[int] = mapped_column(nullable=False)
    """Legacy ID for compatibility with older databases: Integer."""

    tid_old: Mapped[int | None] = mapped_column("TID_old")
    """Legacy TID for compatibility: Integer or None."""

    # Relationships
    type_id: Mapped[int] = mapped_column(
        "type",
        ForeignKey(f"{T_NAME_TYPES}.id"),
        nullable=False,
    )
    """Foreign key referencing the type of the word: Integer."""

    type: Mapped[BaseType] = relationship(
        foreign_keys=[type_id],
        back_populates="words",
        lazy="joined",  # required for proper loading affixes and complexes
    )
    """Relationship to the BaseType model: BaseType instance."""

    event_start_id: Mapped[int] = mapped_column(
        "event_start",
        ForeignKey(f"{T_NAME_EVENTS}.event_id"),
        nullable=False,
    )
    """Foreign key referencing the start event: Integer."""

    event_start: Mapped[BaseEvent] = relationship(
        foreign_keys=[event_start_id],
        back_populates="appeared_words",
    )
    """Relationship to the BaseEvent model for the start event: BaseEvent instance."""

    event_end_id: Mapped[int | None] = mapped_column(
        "event_end",
        ForeignKey(
            f"{T_NAME_EVENTS}.event_id",
        ),
    )
    """Foreign key referencing the end event: Integer or None."""

    event_end: Mapped[BaseEvent | None] = relationship(
        foreign_keys=[event_end_id],
        back_populates="deprecated_words",
    )
    """Relationship to the BaseEvent model for the end event: BaseEvent instance or None."""

    authors: Mapped[list[BaseAuthor]] = relationship(
        secondary=t_connect_authors,
        back_populates="contribution",
    )
    """List of authors associated with the word: List of BaseAuthor instances."""

    definitions: Mapped[list[BaseDefinition]] = relationship(
        back_populates="source_word",
        cascade="all, delete-orphan",
    )
    """List of definitions for the word: List of BaseDefinition instances."""

    # Word's derivatives
    derivatives: Mapped[list[BaseWord]] = relationship(
        secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.parent_id == id),
        secondaryjoin=(t_connect_words.c.child_id == id),
        back_populates="parents",
    )
    """List of words derived from this word: List of BaseWord instances."""

    # Word's parents
    parents: Mapped[list[BaseWord]] = relationship(
        secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.child_id == id),
        secondaryjoin=(t_connect_words.c.parent_id == id),
        back_populates="derivatives",
    )
    """List of parent words of this word: List of BaseWord instances."""

    @hybrid_property
    def affixes(self) -> list[BaseWord]:
        """This property is a hybrid of a Python property and a SQLAlchemy expression.
        It can be used as a property in Python code or as a column in a SQLAlchemy query.

        Returns:
            list[BaseWord]: A list of affixes that are derived from the word.
        """
        return list(
            filter(lambda child: child.type.type_x == "Affix", self.derivatives)
        )

    @hybrid_property
    def complexes(self) -> list[BaseWord]:
        """This property is a hybrid of a Python property and a SQLAlchemy expression.
        It can be used as a property in Python code or as a column in a SQLAlchemy query
        Returns:
            list[BaseWord]: A list of complexes derived from the word.
        """
        return list(filter(lambda child: child.type.group == "Cpx", self.derivatives))
