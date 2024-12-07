"""
This module contains a basic Word Model.
"""

from __future__ import annotations

import datetime

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship

from .author import BaseAuthor
from .base import BaseModel
from .definition import BaseDefinition
from .event import BaseEvent
from .relationships import (
    t_connect_authors,
    t_connect_words,
)
from .service.annotated_types import str_008, str_064, str_128
from .service.table_names import T_NAME_EVENTS, T_NAME_TYPES, T_NAME_WORDS
from .type import BaseType


class BaseWord(BaseModel):
    """BaseWord model representing a word in the database.

    This class encapsulates the attributes and relationships associated with a word
    in the linguistic database. It serves as a foundational model for managing word
    data, including its origins, types, associated authors, definitions, and
    relationships with other words.

    The `BaseWord` class supports various attributes that provide detailed information
    about each word, including its name, origin, matching criteria, and associated
    events. It also establishes relationships with authors and definitions, allowing
    for efficient querying and management of linguistic data.

    Key Features:
        - Supports unique identification of words with an internal ID.
        - Allows for detailed information about the word's origin and matching criteria.
        - Facilitates relationships with authors, definitions, and other words (derivatives and parents).
        - Provides hybrid properties for easy access to specific types of derivatives (affixes and complexes).

    Examples:
        To create a new word instance:

        .. code-block:: python

            word_example = BaseWord(
                origin='3/3E word | 3/7S palabra | 2/5F parole',
                event_start_id=1,
                id=7418,
                id_old=7291,
                match='34%',
                name='purda',
                origin='3/3E word | 3/7S palabra | 2/5F parole',
                rank='1.0',
                type_id=9,
                year=datetime.date(1975, 1, 1)
            )

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
        """
        Initializes a BaseWord instance.

        This constructor sets up a new word with the provided attributes. It is
        essential for creating instances of the `BaseWord` class, allowing for
        the storage of detailed information about each word in the database.

        Args:
            id_old (int):
                Legacy ID for compatibility with older databases. This field is
                required and cannot be null.

            name (str_064):
                The name of the word. This field is required and must be unique
                within the database.

            type_id (int):
                Foreign key referencing the type of the word. This field is
                required and establishes the relationship with the `BaseType` model.

            event_start_id (int):
                Foreign key referencing the start event associated with the word.
                This field is required.

            event_end_id (int | None, optional):
                Foreign key referencing the end event associated with the word.
                This field is optional and can be set to None if there is no end event.

            tid_old (int | None, optional):
                Legacy TID for compatibility with older databases. This field is
                optional and can be set to None.

            origin (str_128 | None, optional):
                The origin of the word. This field is optional and can be set to
                None if the origin is not known.

            origin_x (str_064 | None, optional):
                Additional origin information. This field is optional and can be
                set to None if no additional information is available.

            match (str_008 | None, optional):
                Matching criteria for the word. This field is optional and can be
                set to None if no specific matching criteria are defined.

            rank (str_008 | None, optional):
                Rank of the word. This field is optional and can be set to None
                if no rank is assigned.

            year (datetime.date | None, optional):
                Year associated with the word. This field is optional and can be
                set to None if the year is not specified.

            notes (dict | None, optional):
                Additional notes about the word, stored as a JSON-encoded dictionary.
                This field is optional and can be set to None if no notes are provided.
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
    """Word's internal ID number.

    This attribute serves as the primary key for the word in the database. It is 
    an integer that uniquely identifies each word entry.

    - **Type**: int
    - **Nullable**: False
    """

    name: Mapped[str_064] = mapped_column(nullable=False)
    """The name of the word.

    This attribute holds the actual word as a string. It is required and must 
    be unique within the database.

    - **Type**: str_064
    - **Max Length**: 64 characters
    - **Nullable**: False
    """

    origin: Mapped[str_128 | None]
    """The origin of the word.

    This attribute provides information about the etymology or source of the word. 
    It is optional and can be set to None if the origin is not known.

    - **Type**: str_128 | None
    - **Max Length**: 128 characters
    - **Nullable**: True
    """

    origin_x: Mapped[str_064 | None]
    """Additional origin information.

    This attribute allows for any supplementary details regarding the word's origin. 
    It is optional and can be set to None if no additional information is available.

    - **Type**: str_064 | None
    - **Max Length**: 64 characters
    - **Nullable**: True
    """

    match: Mapped[str_008 | None]
    """Matching criteria for the word.

    This attribute defines any specific criteria used to match the word in queries 
    or searches. It is optional and can be set to None if no matching criteria are defined.

    - **Type**: str_008 | None
    - **Max Length**: 8 characters
    - **Nullable**: True
    """

    rank: Mapped[str_008 | None]
    """Rank of the word.

    This attribute indicates the importance or classification of the word within 
    a specific context. It is optional and can be set to None if no rank is assigned.

    - **Type**: str_008 | None
    - **Max Length**: 8 characters
    - **Nullable**: True
    """

    year: Mapped[datetime.date | None]
    """Year associated with the word.

    This attribute represents the year that is relevant to the word, such as the 
    year it was coined or first recorded. It is optional and can be set to None 
    if the year is not specified.

    - **Type**: datetime.date | None
    - **Nullable**: True
    """

    notes: Mapped[dict[str, str] | None] = mapped_column(JSON)
    """Additional notes about the word.

    This attribute allows for the storage of any extra information or comments 
    regarding the word, encoded as a JSON dictionary. It is optional and can be 
    set to None if no notes are provided.

    - **Type**: dict[str, str] | None
    - **Nullable**: True
    """

    # Field for legacy database compatibility
    id_old: Mapped[int] = mapped_column(nullable=False)
    """Legacy ID for compatibility with older databases.

    This attribute is used to maintain compatibility with previous versions of the 
    database. It is required and cannot be null.

    - **Type**: int
    - **Nullable**: False
    """

    tid_old: Mapped[int | None] = mapped_column("TID_old")
    """Legacy TID for compatibility.

    This attribute serves as a legacy identifier for compatibility with older 
    database systems. It is optional and can be set to None.

    - **Type**: int | None
    - **Nullable**: True
    """

    # Relationships
    type_id: Mapped[int] = mapped_column(
        "type",
        ForeignKey(f"{T_NAME_TYPES}.id"),
        nullable=False,
    )
    """Foreign key referencing the type of the word.

    This attribute links the word to its type in the database, establishing a 
    relationship with the `BaseType` model. It is required and cannot be null.

    - **Type**: int
    - **Nullable**: False
    """

    type: Mapped[BaseType] = relationship(
        foreign_keys=[type_id],
        back_populates="words",
        lazy="joined",  # required for proper loading affixes and complexes
    )
    """Relationship to the BaseType model.

        This attribute establishes a relationship with the `BaseType` model, allowing 
        access to the type associated with the word. It is populated based on the 
        `type_id` foreign key, which links to the primary key of the `BaseType` table.

        - **Type**: BaseType
        - **Nullable**: False
        - **Back Population**: This relationship is bidirectional, allowing access to 
          all words associated with a given type through the `words` attribute in 
          the `BaseType` model.
        - **Loading Strategy**: The relationship uses a "joined" loading strategy, 
          which means that the related `BaseType` instance is loaded in the same 
          query as the `BaseWord` instance for efficiency.
    """
    event_start_id: Mapped[int] = mapped_column(
        "event_start",
        ForeignKey(f"{T_NAME_EVENTS}.event_id"),
        nullable=False,
    )
    """Foreign key referencing the start event.

        This attribute links the word to the event during which it was first recorded 
        or used. It is required and cannot be null.

        - **Type**: int
        - **Nullable**: False
    """

    event_start: Mapped[BaseEvent] = relationship(
        foreign_keys=[event_start_id],
        back_populates="appeared_words",
    )
    """Relationship to the BaseEvent model for the start event.

        This attribute establishes a relationship with the `BaseEvent` model, allowing 
        access to the event during which the word first appeared. It is automatically 
        populated based on the `event_start_id`.

        - **Type**: BaseEvent
        - **Nullable**: False
    """

    event_end_id: Mapped[int | None] = mapped_column(
        "event_end",
        ForeignKey(
            f"{T_NAME_EVENTS}.event_id",
        ),
    )
    """Foreign key referencing the end event.

        This attribute links the word to the event during which it was deprecated or 
        no longer in use. It is optional and can be set to None if there is no end event.

        - **Type**: int | None
        - **Nullable**: True
    """

    event_end: Mapped[BaseEvent | None] = relationship(
        foreign_keys=[event_end_id],
        back_populates="deprecated_words",
    )
    """Relationship to the BaseEvent model for the end event.

        This attribute establishes a relationship with the `BaseEvent` model, allowing 
        access to the event during which the word was deprecated. It is automatically 
        populated based on the `event_end_id`.

        - **Type**: BaseEvent | None
        - **Nullable**: True
    """

    authors: Mapped[list[BaseAuthor]] = relationship(
        secondary=t_connect_authors,
        back_populates="contribution",
    )
    """List of authors associated with the word.

    This attribute establishes a many-to-many relationship with the `BaseAuthor` 
    model, allowing for the retrieval of all authors who have contributed to the 
    word. It is populated based on the association table `t_connect_authors`.

    - **Type**: list[BaseAuthor]
    - **Nullable**: True
    """

    definitions: Mapped[list[BaseDefinition]] = relationship(
        back_populates="source_word",
        cascade="all, delete-orphan",
    )
    """List of definitions for the word.

        This attribute establishes a one-to-many relationship with the `BaseDefinition` 
        model, allowing for the retrieval of all definitions associated with the word. 
        It is populated based on the relationship defined in the `BaseDefinition` model.

        - **Type**: list[BaseDefinition]
        - **Nullable**: True
    """

    # Word's derivatives
    derivatives: Mapped[list[BaseWord]] = relationship(
        secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.parent_id == id),
        secondaryjoin=(t_connect_words.c.child_id == id),
        back_populates="parents",
    )
    """List of words derived from this word.

        This attribute establishes a many-to-many relationship with other `BaseWord` 
        instances, allowing for the retrieval of all words that are derived from the 
        current word. It is populated based on the association table `t_connect_words`.

        - **Type**: list[BaseWord]
        - **Nullable**: True
    """

    # Word's parents
    parents: Mapped[list[BaseWord]] = relationship(
        secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.child_id == id),
        secondaryjoin=(t_connect_words.c.parent_id == id),
        back_populates="derivatives",
    )
    """List of parent words of this word.

        This attribute establishes a many-to-many relationship with other `BaseWord` 
        instances, allowing for the retrieval of all parent words from which the current 
        word is derived. It is populated based on the association table `t_connect_words`.

        - **Type**: list[BaseWord]
        - **Nullable**: True
    """

    @property
    def affixes(self) -> list[BaseWord]:
        """List of affixes derived from the word.

        This property filters the derivatives to return only those that are classified
        as affixes.

        Returns:
            list[BaseWord]: A list of affixes that are derived from the word.
        """
        return list(
            filter(lambda child: child.type.type_x == "Affix", self.derivatives)
        )

    @property
    def complexes(self) -> list[BaseWord]:
        """List of complexes derived from the word.

        This property filters the derivatives to return only those that are classified
        as complexes.

        Returns:
            list[BaseWord]: A list of complexes that are derived from the word.
        """
        return list(filter(lambda child: child.type.group == "Cpx", self.derivatives))
