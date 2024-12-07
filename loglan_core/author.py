"""
This module contains a basic Author Model
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import BaseModel
from .relationships import t_connect_authors
from .service.annotated_types import str_064, str_128
from .service.table_names import T_NAME_AUTHORS

if TYPE_CHECKING:
    from .word import BaseWord


class BaseAuthor(BaseModel):
    """Base Author's Database Model.

    This class represents an author in the database, encapsulating the
    attributes and relationships associated with authors of words. It
    serves as a foundational model for managing author data, including
    their abbreviations, full names, and any additional notes.

    The :class:`~loglan_core.author.BaseAuthor` class establishes a many-to-many
    relationship with the :class:`~loglan_core.word.BaseWord` class through the
    :class:`~loglan_core.relationships.t_connect_authors` association table,
    allowing for efficient querying and management of authors and their
    contributions to various words.

    Key Features:
        - Supports unique abbreviations for each author.
        - Allows optional full names and notes for additional context.
        - Facilitates relationships with words, enabling easy access to
          all words associated with a given author.

    Examples:
        .. code-block:: python

            {
                'id': 13, 'full_name': 'James Cooke Brown',
                'abbreviation': 'JCB', 'notes': ''
            },
            {
                'id': 29, 'full_name': 'Loglan 4&5', 'abbreviation': 'L4',
                'notes': 'The printed-on-paper book, 1975 version of the dictionary.'
             }

    Attributes:
        abbreviation (Mapped[str_064]): A unique abbreviation for the author.
        full_name (Mapped[str_064 | None]): The full name of the author, if available.
        notes (Mapped[str_128 | None]): Additional notes about the author.
        contribution (Mapped[list[BaseWord]]): A list of words associated with the author.
    """

    __tablename__ = T_NAME_AUTHORS

    def __init__(
        self,
        abbreviation: Mapped[str_064],
        full_name: Mapped[str_064 | None],
        notes: Mapped[str_128 | None],
    ):
        """Initializes a BaseAuthor instance.

        This constructor sets up a new author with the provided abbreviation,
        full name, and optional notes. The abbreviation must be unique and is
        used in the LOD (Loglan Online Dictionary) dictionary. The full name
        and notes are optional and can be used to provide additional context
        about the author.

        Args:
            abbreviation (Mapped[str_064]):
                A unique abbreviation for the author, used for identification
                in various contexts, including the LOD dictionary. This field
                is required and cannot be null.

            full_name (Mapped[str_064 | None], optional):
                The full name of the author. This field is optional and can be
                set to None if the full name is not available.

            notes (Mapped[str_128 | None], optional):
                Any additional information or notes about the author. This field
                is also optional and can be set to None if no notes are provided.

        Examples:
            To create a new author instance:

            .. code-block:: python

                author_jcb = BaseAuthor(abbreviation='JCB', full_name='James Cooke Brown')
                author_l4 = BaseAuthor(abbreviation='L4', full_name='Loglan 4&5',
                notes='The printed-on-paper book, 1975 version of the dictionary.')
        """
        super().__init__()
        self.abbreviation = abbreviation
        self.full_name = full_name
        self.notes = notes

    def __str__(self):
        """Returns a string representation of the BaseAuthor instance.

        Returns:
            str: A string representing the instance with class name,
            author's ID (if available), and abbreviation.
        """
        return (
            f"<{self.__class__.__name__}"
            f"{' ID ' + str(self.id) + ' ' if self.id else ' '}"
            f"{self.abbreviation}>"
        )

    abbreviation: Mapped[str_064] = mapped_column(nullable=False, unique=True)
    """The abbreviation for the author, used in the LOD.

    This field is required and must be unique for each author. It helps in identifying 
    the author in various contexts, including databases and references.

    - **Type**: :class:`~loglan_core.base.str_064`
    - **Max Length**: 64 characters
    - **Nullable**: False (this field cannot be empty)
    - **Unique**: True (no two authors can have the same abbreviation)

    Examples:
        - ``JCB``: Abbreviation for James Cooke Brown
        - ``L4``: Abbreviation for Loglan 4&5
    """

    full_name: Mapped[str_064 | None]
    """The full name of the author, if available.

    This field is optional and can be left empty if the author's full name is not known. 
    It provides additional context about the author and can be used in various references.

    - **Type**: :class:`~loglan_core.base.str_064 | None`
    - **Max Length**: 64 characters
    - **Nullable**: True (this field can be empty)
    - **Unique**: False (multiple authors can have the same full name)

    Examples:
        - ``James Cooke Brown``: Full name of the author known for his contributions to linguistics.
        - ``Loglan 4&5``: Full name associated with the Loglan language.
    """

    notes: Mapped[str_128 | None]
    """Additional information or notes about the author, if available.

    This field is optional and can be used to provide any relevant details or context 
    about the author that may not be captured in other fields. It can be left empty if 
    no additional information is provided.

    - **Type**: :class:`~loglan_core.base.str_128 | None`
    - **Max Length**: 128 characters
    - **Nullable**: True (this field can be empty)
    - **Unique**: False (multiple authors can have the same notes)

    Examples:
        - ``Notable linguist with contributions to Loglan.``: 
        A brief note about the author's significance.
        - ``Authors of the 1975 version of the dictionary.``: 
        Additional context regarding the author's work.
    """

    contribution: Mapped[list[BaseWord]] = relationship(
        back_populates="authors",
        secondary=t_connect_authors,
    )
    """Establishes a many-to-many relationship between the author and their associated words.

    This attribute connects the :class:`~loglan_core.author.BaseAuthor` to multiple 
    :class:`~loglan_core.word.BaseWord` instances through the 
    :class:`~loglan_core.relationships.t_connect_authors` secondary table. 
    This relationship allows for efficient querying of all words associated with a given author.

    - **Type**: Mapped[list[:class:`~loglan_core.word.BaseWord`]]
    - **Relationship**: Many-to-many (an author can contribute to multiple words, 
    and a word can have multiple authors)
    - **Back Population**: This relationship is bidirectional, 
    allowing access to the authors from the words.

    Returns:
        Mapped[list[BaseWord]]: A list of :class:`~loglan_core.word.BaseWord` 
        instances that are associated with the current author instance.
    """
