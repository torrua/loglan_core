"""
This module contains a basic Author Model
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from loglan_core.base import BaseModel, str_064, str_128
from loglan_core.connect_tables import t_connect_authors
from loglan_core.table_names import T_NAME_AUTHORS

if TYPE_CHECKING:
    from loglan_core.word import BaseWord

__pdoc__ = {
    "BaseAuthor.created": False,
    "BaseAuthor.updated": False,
}


class BaseAuthor(BaseModel):
    """Base Author's DB Model

    Describes a table structure for storing information about word authors.

    This class connects with words using a "many-to-many" relationship using `t_connect_authors`.

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

    """

    __tablename__ = T_NAME_AUTHORS

    def __init__(
        self,
        abbreviation: Mapped[str_064],
        full_name: Mapped[str_064 | None],
        notes: Mapped[str_128 | None],
    ):
        """Initializes a BaseAuthor instance.

        Args:
            abbreviation (str): Author's abbreviation (used in the LOD dictionary).
            full_name (str, optional): Author's full name if it exists.
            notes (str, optional): Any additional information about the author.
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
    """Author's abbreviation (used in the LOD dictionary).
    
    :type: :class:`~loglan_core.base.str_064` with max_length=64, nullable=False, unique=True

    Examples:
        ``JCB``, ``L4``
    """

    full_name: Mapped[str_064 | None]
    """Author's full name if it exists.
    
    :type: :class:`~loglan_core.base.str_064` with max_length=64, nullable=True, unique=False

    Examples:
        ``James Cooke Brown``, ``Loglan 4&5``
    """

    notes: Mapped[str_128 | None]
    """Additional information (notes) if it exists.
    
    :type: :class:`~loglan_core.base.str_128` with max_length=128, nullable=True, unique=False
    """

    contribution: Mapped[list[BaseWord]] = relationship(
        back_populates="authors",
        secondary=t_connect_authors,
    )
    """
    This is a relationship that establishes a 'many-to-many' 
    connection between the Author and his Words. 
    It is done via the :class:`~loglan_core.connect_tables.t_connect_authors`
     secondary table and does not enable typechecks.

    Returns:
        Mapped[list[BaseWord]]: A list of BaseWord instances associated with the current instance.
    """
