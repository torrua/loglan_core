# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a basic Author Model
"""
from __future__ import annotations

from typing import List

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from loglan_core.base import BaseModel, str_064, str_128
from loglan_core.connect_tables import t_connect_authors
from loglan_core.table_names import T_NAME_AUTHORS

__pdoc__ = {
    "BaseAuthor.created": False,
    "BaseAuthor.updated": False,
}


class BaseAuthor(BaseModel):
    """Base Author's DB Model

    Describes a table structure for storing information about words authors.

    Connects with words with "many-to-many" relationship. See `t_connect_authors`.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 13, 'full_name': 'James Cooke Brown',
    'abbreviation': 'JCB', 'notes': ''}

    {'id': 29, 'full_name': 'Loglan 4&5',
    'abbreviation': 'L4',
    'notes': 'The printed-on-paper book,
              1975 version of the dictionary.'}
    ```
    </p></details>
    """

    __tablename__ = T_NAME_AUTHORS

    def __init__(
        self,
        abbreviation: Mapped[str_064],
        full_name: Mapped[str_064 | None],
        notes: Mapped[str_128 | None],
    ):
        super().__init__()
        self.abbreviation = abbreviation
        self.full_name = full_name
        self.notes = notes

    def __repr__(self):
        """
        Returns:
        """
        return (
            f"<{self.__class__.__name__}"
            f"{' ID ' + str(self.id) + ' ' if self.id else ' '}"
            f"{self.abbreviation}>"
        )

    abbreviation: Mapped[str_064] = mapped_column(nullable=False, unique=True)
    """*Author's abbreviation (used in the LOD dictionary)*  
        **str** : max_length=64, nullable=False, unique=True
    Example:
        > JCB, L4
    """

    full_name: Mapped[str_064 | None]
    """
    *Author's full name (if exists)*  
        **str** : max_length=64, nullable=True, unique=False
    Example:
        > James Cooke Brown, Loglan 4&5
    """

    notes: Mapped[str_128 | None]
    """*Any additional information about author*  
        **str** : max_length=128, nullable=True, unique=False
    """

    _contribution: Mapped[List["BaseWord"]] = relationship(  # type: ignore
        back_populates="_authors",
        secondary=t_connect_authors,
        enable_typechecks=False,
    )

    @property
    def contribution(self) -> list:
        """
        *Relationship query for getting a list of words coined by this author*
         **query** : Optional[List[BaseWord]]
        """
        return self._contribution
